"""
Simple pydantic models for the Coefficient model.
"""

from pydantic import BaseModel


class PydanticCoefficientModelFromJSON(BaseModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    academic_year: int
    multiplier: float
    course_type_id: int
    status_id: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True