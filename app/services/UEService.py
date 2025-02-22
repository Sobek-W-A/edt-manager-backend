"""
UE-related operations service.
Provides the methods to use when interacting with an UE.
"""
from fastapi import HTTPException

from app.models.pydantic.CourseModel import PydanticCourseModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel
from app.models.pydantic.UEModel import PydanticCreateUEModel, PydanticUEModel, PydanticModifyUEModel
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.course import CourseInDB
from app.models.tortoise.course_type import CourseTypeInDB
from app.models.tortoise.node import NodeInDB
from app.models.tortoise.ue import UEInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations

async def get_ue_by_id(ue_id: int, current_account: AccountInDB) -> PydanticUEModel:
    """
    This method returns the UE of the given UE id.
    """

    # todo :ACADEMIC_YEAR A RAJOUTE A L AVENIR

    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    ue: UEInDB | None = await UEInDB.get_or_none(id=ue_id).prefetch_related("courses__course_type")

    if ue is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    courses: list[CourseInDB] | None = await ue.courses.all()

    courses_pydantic: list[PydanticCourseModel] = []

    for course in courses:
        course_type: CourseTypeInDB | None = await CourseTypeInDB.get_or_none(id=course.course_type_id)
        course_type_pydantic = PydanticCourseTypeModel.model_validate(course_type)
        course_pydantic = PydanticCourseModel(
            academic_year=course.academic_year,
            id=course.id,
            duration=course.duration,
            group_count=course.group_count,
            course_type=course_type_pydantic,
        )
        courses_pydantic.append(course_pydantic)

    return PydanticUEModel(academic_year=ue.academic_year,
                           courses=courses_pydantic,
                           name=ue.name,
                           ue_id=ue.id)


async def add_ue(body: PydanticCreateUEModel, current_account: AccountInDB) -> None:
    """
    This method creates a new UE.
    """

    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)
    
    parent_node: NodeInDB | None = await NodeInDB.get_or_none(id=body.parent_id)
    if parent_node is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)

    if await NodeInDB.filter(parent_id=body.parent_id).exists():
        raise HTTPException(status_code=409,
                            detail=CommonErrorMessages.FOLDER_AND_UE_NOT_ENABLED.value)


    ue_to_create: UEInDB = UEInDB(name=body.name,
                                  academic_year=body.academic_year,
                                  parent=parent_node)

    await UEInDB.save(ue_to_create)

    created_courses : list[CourseInDB] = []
    if body.courses:
        for course_data in body.courses:
            course = await CourseInDB.create(
                academic_year=course_data.academic_year,
                duration=course_data.duration,
                group_count=course_data.group_count,
                course_type_id=course_data.course_type_id,
            )
            created_courses.append(course)

    await ue_to_create.courses.add(*created_courses)




async def modify_ue(ue_id: int, body: PydanticModifyUEModel, current_account: AccountInDB) -> None:
    """
    This method modifies the UE of the given UE id.
    """

    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    ue_to_modify: UEInDB | None = await UEInDB.get_or_none(id=ue_id)

    if ue_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    if await UEInDB.filter(name=body.name).exists():
        raise HTTPException(status_code=409, detail=CommonErrorMessages.UE_ALREADY_EXIST.value)

    try:
        await ue_to_modify.update_from_dict(body.model_dump(exclude_none=True)) # type: ignore
        await ue_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return None


async def delete_ue(ue_id: int, current_account: AccountInDB) -> None:
    """
    This method deletes the UE of the given UE id.
    """

    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.DELETE,
                            current_account)

    ue: UEInDB | None = await UEInDB.get_or_none(id=ue_id)

    if ue is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    await ue.delete()

async def attach_ue_to_node(ue_id: int, node_id: int, academic_year: int, current_account: AccountInDB) -> None:
    """
    This method marks the node provided as the parent for the UE.
    """
    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account,
                            academic_year)
    
    ue: UEInDB | None = await UEInDB.get_or_none(id=ue_id)
    if ue is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)
    
    node: NodeInDB | None = await NodeInDB.get_or_none(id=node_id)
    if node is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.NODE_NOT_FOUND.value)
    
    if await NodeInDB.filter(parent_id=node_id).exists():
        raise HTTPException(status_code=409, detail=CommonErrorMessages.FOLDER_AND_UE_NOT_ENABLED.value)
    
    await ue.parent.add(node)
    await ue.save()


async def detach_ue_from_node(ue_id: int, node_id: int, academic_year: int, current_account: AccountInDB) -> None:
    """
    This method removes the parent node from the UE.
    """
    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account,
                            academic_year)
    
    ue: UEInDB | None = await UEInDB.get_or_none(id=ue_id)
    if ue is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)
    
    node: NodeInDB | None = await NodeInDB.get_or_none(id=node_id)
    if node is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.NODE_NOT_FOUND.value)
    
    await ue.parent.remove(node)
    await ue.save()
