from fastapi import HTTPException

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.CourseModel import PydanticCourseModel, PydanticCreateCourseModel, PydanticModifyCourseModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel

from app.models.tortoise.course import CourseInDB
from app.models.tortoise.course_type import CourseTypeInDB
from app.services.PermissionService import check_permissions

from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations

#TODO


async def get_course_by_id(course_id: int, current_account: AuthenticatedAccount) -> PydanticCourseModel:
    """
        This method retrieves course from id.
        """

    await check_permissions(AvailableServices.COURSE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    course: CourseInDB | None = await CourseInDB.get_or_none(id=course_id).prefetch_related("course_type")

    if course is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND.value)

    course_type = PydanticCourseTypeModel.model_validate(course.course_type)

    return PydanticCourseModel(academic_year=course.academic_year,
                               id=course.id,
                               duration=course.duration,
                               group_count=course.group_count,
                               course_type=course_type)


async def add_course(body: PydanticCreateCourseModel, current_account: AuthenticatedAccount) -> PydanticCourseModel:
    """
    This method creates a new course.
    """

    await check_permissions(AvailableServices.COURSE_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)

    if body.group_count < 0:
        raise HTTPException(status_code=422, detail=CommonErrorMessages.GROUP_VALUE_INCORRECT.value)

    course_type: CourseTypeInDB = await CourseTypeInDB.get_or_none(id=body.course_type_id)

    if course_type is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_TYPE_NOT_FOUND.value)

    course_type_pydantic = PydanticCourseTypeModel.model_validate(course_type)

    course_to_create: CourseInDB = CourseInDB(academic_year=body.academic_year, duration=body.duration,
                                              group_count=body.group_count, course_type_id=body.course_type_id)

    await CourseInDB.save(course_to_create)

    return PydanticCourseModel(academic_year=course_to_create.academic_year,
                               id=course_to_create.id,
                               duration=course_to_create.duration,
                               group_count=course_to_create.group_count,
                               course_type=course_type_pydantic)


async def modify_course(course_id: int, body: PydanticModifyCourseModel, current_account: AuthenticatedAccount) -> None:
    """
    This method modifies the course of the given course id.
    """

    await check_permissions(AvailableServices.COURSE_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    if body.duration is not None:
        if body.duration < 0:
            raise HTTPException(status_code=422, detail=CommonErrorMessages.DURATION_VALUE_INCORRECT.value)

    if body.group_count is not None:
        if body.group_count < 0:
            raise HTTPException(status_code=422, detail=CommonErrorMessages.GROUP_VALUE_INCORRECT.value)

    course_to_modify: CourseInDB | None = await CourseInDB.get_or_none(id=course_id)

    if course_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND.value)

    try:
        await course_to_modify.update_from_dict(body.model_dump(exclude_none=True))
        await course_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


async def delete_course(course_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This method delete the course of the given course id.
    """
    await check_permissions(AvailableServices.COURSE_SERVICE,
                            AvailableOperations.DELETE,
                            current_account)

    course: CourseInDB | None = await CourseInDB.get_or_none(id=course_id)

    if course is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.UE_NOT_FOUND.value)

    await course.delete()
