"""
Pydantic models for Course.
"""

from pydantic import BaseModel
from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel


class PydanticCourseModelFromJSON(BaseModel):
    """
    Course model for loading data from a JSON file.
    """
    duration        : int
    academic_year   : int
    course_type_id  : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True

class PydanticCourseModel(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to return a Course to the frontend.
    """
    course_id: int
    duration : int
    courses_types : list[PydanticCourseTypeModel]

