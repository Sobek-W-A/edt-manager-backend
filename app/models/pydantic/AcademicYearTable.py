"""
Pydantic models for the PydanticAcademicTable model.
"""
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