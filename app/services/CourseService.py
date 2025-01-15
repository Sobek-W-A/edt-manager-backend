from fastapi import HTTPException

from app.models.pydantic.CourseModel import PydanticCourseModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel

from app.models.tortoise.course import CourseInDB

from app.utils.enums.http_errors import CommonErrorMessages


async def get_course_by_id(course_id: int) -> PydanticCourseModel:
    """
        This method retrieves course from id.
        """

    course: CourseInDB = await CourseInDB.get_or_none(id=course_id)

    if course is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COURSE_NOT_FOUND.value)

    course_type = PydanticCourseTypeModel(
        name=course.course_type.name,
        description=course.course_type.description,
        group_count=course.course_type.group_count,
        academic_year=course.course_type.academic_year
    )

    return PydanticCourseModel(academic_year=course.academic_year,
                               duration=course.duration,
                               course_id=course.id,
                               courses_type=course_type)


async def add_course(body: PydanticCourseModel) -> PydanticCourseModel:
    """
    This method creates a new course.
    """

    #TODO


async def modify_course(course_id: int, body: PydanticCourseModel) -> None:
    """
    This method modifies the course of the given course id.
    """

    #TODO

    return None
