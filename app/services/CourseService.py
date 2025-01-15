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

    print(course.course_type)

    course_type = PydanticCourseTypeModel(
        course_type_id=course.course_type.id,
        name=course.course_type.name,
        description=course.course_type.description,
        academic_year=course.course_type.academic_year
    )

    return PydanticCourseModel(academic_year=course.academic_year,
                               duration=course.duration,
                               course_id=course.id,
                               group_count=course.group_count,
                               courses_type=[course_type])


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
