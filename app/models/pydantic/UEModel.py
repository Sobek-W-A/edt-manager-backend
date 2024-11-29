"""
Pydantic UE models.
"""
from typing import Optional

from pydantic import BaseModel
from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.CourseModel import PydanticCourseModel


class PydanticUEModelFromJSON(BaseModel):
    """
    Pydantic model for loading data from a JSON file.
    """
    name           : str
    courses_id_m2m : list[int]
    academic_year  : int
    parent_id      : int | None

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
    name: str
    courses: Optional[list[PydanticCourseModel]]
