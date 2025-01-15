"""
Pydantic models for Course.
"""
from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel


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
    course_type : list[PydanticCourseTypeModel]
