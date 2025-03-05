"""
This module provides pydantic models for the Status.
"""
from app.models.pydantic.CoefficientModel import PydanticCoefficientModelResponse
from app.models.pydantic.abstract.ClassicModel import ClassicModel


class PydanticStatusResponseModel(ClassicModel):
    """
    Simple Pydantic model to represent a status.
    """
    id   : int
    quota: int
    multiplier : list[PydanticCoefficientModelResponse]

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True

class PydanticStatusModelFromJSON(ClassicModel):
    """
    Pydantic model for status. Used to load data from JSON files.
    """
    quota         : int

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True

class PydanticStatusExportModel(ClassicModel):
    """
    Pydantic model for exporting status to JSON.
    """
    id   : int
    quota: int

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True
