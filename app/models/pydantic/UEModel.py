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


class PydanticUEModel(AcademicYearPydanticModel):

    ue_id: int
    name: str
    courses: list[PydanticCourseModel]

class PydanticCreateUEModel(AcademicYearPydanticModel):

    name: str
    courses: Optional[list[PydanticCourseModel]]



    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True
