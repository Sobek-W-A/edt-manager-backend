from app.models.pydantic.CourseModel import PydanticCourseModel

from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.course import CourseInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations

async def get_courses_from_module(module_id: int) -> list[PydanticCourseModel]:
    """
        This method retrieves all courses from a module.
        """

    courses = await CourseInDB.get_courses_from_module(module_id)

    return courses

    #TODO

async def create_course(module_id: int) -> None:
    """
        This method retrieves all courses from a module.
    """
        #TODO

async def delete_course(module_id: int) -> None:


    #TODO

async def modify_course(module_id: int) -> None:

    #TODO




