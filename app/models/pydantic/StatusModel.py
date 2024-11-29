"""
This module provides pydantic models for the Status.
"""

from pydantic import BaseModel
from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel


class PydanticStatusResponseModel(AcademicYearPydanticModel):
    """
    Simple Pydantic model to represent a status.
    """
    name        : str
    description : str

class PydanticStatusModelFromJSON(BaseModel):
    """
    Pydantic model for status. Used to load data from JSON files.
    """
    name          : str
    description   : str
    academic_year : int

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes = True
