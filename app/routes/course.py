"""
Courses routes.
Used to manage course operations.
"""

# TODO

from fastapi import APIRouter

from app.models.pydantic.CourseModel import PydanticCourseModel
from app.routes.tags import Tag
from app.services import CourseService

courseRouter: APIRouter = APIRouter(prefix="/course")
tag: Tag = {
    "name": "Course",
    "description": "Course-related operations."
}


@courseRouter.get("/{course_id}",status_code=200, response_model=None)
async def get_course_by_id(course_id: int) -> PydanticCourseModel:
    """
    This method returns the course of the given course id.
    """
    return await CourseService.get_course_by_id(course_id)



@courseRouter.post("/", status_code=201, response_model=None)
async def add_course(body : PydanticCourseModel) -> None:
    """
    This method creates a new course.
    """
    await CourseService.add_course(body)

@courseRouter.patch("/{course_id}", status_code=205)
async def modify_course(course_id: int, body: PydanticCourseModel) -> None:
    """
    This method modifies the course of the given course id.
    """
    await CourseService.modify_course(course_id,body)


@courseRouter.delete("/{course_id}", status_code=204)
async def delete_course(course_id: int) -> None:
    """
    This method deletes the course of the given course id.
    """

    #TODO
    return None
