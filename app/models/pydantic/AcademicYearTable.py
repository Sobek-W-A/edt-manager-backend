"""
Pydantic models for the PydanticAcademicTable model.
"""
from pydantic import BaseModel

from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel


class PydanticAcademicTableModel(AcademicYearPydanticModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    id    : int
    description : str

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticAcademicYearTableModelFromJSON(BaseModel):
    """
    Pydantic Model for Academic year. This model is used to validate and transform JSON data.
    """
    id: int
    description: str
    academic_year: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True