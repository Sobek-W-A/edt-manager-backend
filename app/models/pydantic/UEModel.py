"""
This module provides the UEPydanticModel class.
"""
from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel


class UEPydanticModel(AcademicYearPydanticModel):

    ue_id: int
    name: str
