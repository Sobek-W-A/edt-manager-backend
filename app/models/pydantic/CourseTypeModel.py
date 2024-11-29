"""
Pydantic models for CourseType.
"""

from pydantic import BaseModel

from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel


class PydanticCourseTypeModel(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to return a CourseType to the frontend.
    """
    name:str
    description : str

class PydanticCourseTypeModelFromJSON(BaseModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    name         : str
    description  : str
    academic_year: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
