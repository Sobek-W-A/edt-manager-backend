"""
Course_types routes.
Used to manage course_type operations.
"""

# TODO

from fastapi import APIRouter

from app.routes.tags import Tag


coursetypeRouter: APIRouter = APIRouter(prefix="/course_type")
tag: Tag = {
    "name": "CourseType",
    "description": "CourseType-related operations."
}


@coursetypeRouter.get("/",status_code=200, response_model=None)
async def get_course_type(body : None) -> None:
    """
    This method returns all course types.
    """
    return None

@coursetypeRouter.get("/{course_type_id}",status_code=200, response_model=None)
async def get_course_type_by_id(course_id: int) -> None:
    """
    This method returns the course type of the given course type id.
    """
    return None

@coursetypeRouter.post("/", status_code=201, response_model=None)
async def add_course_type() -> None:
    """
    This method creates a new course type.
    """
    return None

@coursetypeRouter.patch("/{course_type_id}", status_code=205)
async def modify_course_type(course_id: int, body: None) -> None:
    """
    This method modifies the course type of the given course type id.
    """
    return None


@coursetypeRouter.delete("/{course_type_id}", status_code=204)
async def delete_course_type(course_id: int) -> None:
    """
    This method deletes the course type of the given course type id.
    """
    return None