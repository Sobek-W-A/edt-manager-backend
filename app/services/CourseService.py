from app.models.pydantic.CourseModel import PydanticCourseModel

from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.course import CourseInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations

async def get_courses_from_id(course_id: int) -> PydanticCourseModel:
    """
        This method retrieves course from id.
        """

    course = await CourseInDB.get_or_none(id=course_id)

    return course








