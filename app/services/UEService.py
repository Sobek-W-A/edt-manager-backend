"""
UE-related operations service.
Provides the methods to use when interacting with an UE.
"""
from fastapi import HTTPException

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.CourseModel import PydanticCourseModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel
from app.models.pydantic.UEModel import PydanticCreateUEModel, PydanticUEModel, PydanticModifyUEModel
from app.models.tortoise.course import CourseInDB
from app.models.tortoise.course_type import CourseTypeInDB
from app.models.tortoise.ue import UEInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations
#TODO

async def get_ue_by_id(ue_id: int, current_account=AuthenticatedAccount) -> PydanticUEModel:
    """
    This method returns the UE of the given UE id.
    """

    #ACADEMIC_YEAR A RAJOUTE A L AVENIR

    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    ue: UEInDB | None = await UEInDB.get_or_none(id=ue_id).prefetch_related("courses__course_type")

    if ue is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    courses: list[CourseInDB] | None = await ue.courses.all()

    coursesPydantic: list[PydanticCourseModel] = []

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
        coursesPydantic.append(course_pydantic)

    return PydanticUEModel(academic_year=ue.academic_year,
                           courses=coursesPydantic,
                           name=ue.name,
                           ue_id=ue.id)


async def add_ue(body: PydanticCreateUEModel, current_account=AuthenticatedAccount) -> PydanticUEModel:
    """
    This method creates a new UE.
    """

    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)

    ue_to_create: UEInDB = UEInDB(name=body.name, academic_year=body.academic_year)

    await UEInDB.save(ue_to_create)

    return PydanticUEModel(academic_year=body.academic_year,
                           courses=[],
                           name=body.name,
                           ue_id=ue_to_create.id)


async def modify_ue(ue_id: int, body: PydanticModifyUEModel, current_account=AuthenticatedAccount) -> None:
    """
    This method modifies the UE of the given UE id.
    """

    await check_permissions(AvailableServices.UE_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    ue_to_modify: UEInDB = await UEInDB.get_or_none(id=ue_id)

    if ue_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    if await UEInDB.filter(name=body.name).exists():
        raise HTTPException(status_code=409, detail=CommonErrorMessages.UE_ALREADY_EXIST.value)

    try:
        await ue_to_modify.update_from_dict(body.model_dump(exclude_none=True))
        await ue_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return None


async def delete_ue(ue_id: int, current_account=AuthenticatedAccount) -> None:
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
