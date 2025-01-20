"""
Pydantic models for Course.
"""

from typing import Optional
from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel
from app.models.pydantic.tools.validator import Hours


class PydanticCourseModelFromJSON(AcademicYearPydanticModel):
    """
    Course model for loading data from a JSON file.
    """
    duration        : int
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
    id: int
    duration : int
    group_count : int
    course_type : PydanticCourseTypeModel

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticCreateCourseModel(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to create a Course.
    """
    duration : int
    group_count : int
    course_type_id : int

class PydanticModifyCourseModel(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to modify a Course.
    """
    academic_year: Optional[int] = None
    duration : Optional[Hours] = None
    group_count : Optional[int] = None
    course_type_id : Optional[int] = None