"""
This module provides pydantic models for the Status.
"""

from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel


class PydanticStatusResponseModel(AcademicYearPydanticModel):
    """
    Simple Pydantic model to represent a status.
    """
    status  : str
    message : str
