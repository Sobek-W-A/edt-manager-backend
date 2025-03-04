"""
Simple pydantic models for the Coefficient model.
"""
from pydantic import BaseModel

from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel


class PydanticCoefficientModelFromJSON(BaseModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    multiplier: float
    course_type_id: int
    status_id: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticCoefficientModelResponse(BaseModel):
    """
    This class is used to response to a Pydantic model.
    """
    multiplier: float
    course_type: PydanticCourseTypeModel

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True