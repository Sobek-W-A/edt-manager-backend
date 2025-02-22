"""
Pydantic UE models.
"""
from typing import Optional

from pydantic import BaseModel
from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.CourseModel import PydanticCourseModel, PydanticCreateCourseModel


class PydanticUEModelFromJSON(BaseModel):
    """
    Pydantic model for loading data from a JSON file.
    """
    name         : str
    courses_m2m  : list[int]
    academic_year: int
    parent_m2m   : list[int] | None

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True


class PydanticUEModel(AcademicYearPydanticModel):
    """
    Pydantic model for UE to send to the Frontend.
    """
    ue_id: int
    name: str
    courses: list[PydanticCourseModel]


class PydanticCreateUEModel(AcademicYearPydanticModel):
    """
    Pydantic model for UE to create an UE.
    """
    name      : str
    parent_id : int
    courses   : Optional[list[PydanticCreateCourseModel]]

class PydanticModifyUEModel(AcademicYearPydanticModel):
    """
    Pydantic model for UE to create an UE.
    """
    name      : str
