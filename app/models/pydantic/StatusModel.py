"""
This module provides pydantic models for the Status.
"""
from app.models.pydantic.abstract.ClassicModel import ClassicModel
from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel


class PydanticStatusResponseModel(AcademicYearPydanticModel, ClassicModel):
    """
    Simple Pydantic model to represent a status.
    """
    quota         : int

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True

class PydanticStatusModelFromJSON(AcademicYearPydanticModel, ClassicModel):
    """
    Pydantic model for status. Used to load data from JSON files.
    """
    quota         : int

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True
