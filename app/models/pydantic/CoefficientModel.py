"""
Simple pydantic models for the Coefficient model.
"""
from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel


class PydanticCoefficientModelFromJSON(AcademicYearPydanticModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    multiplier: float
    course_type_id: int
    status_id: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticCoefficientExportModel(AcademicYearPydanticModel):
    """
    This class is used to export a Pydantic model to a JSON file.
    """
    multiplier: float
    course_type_id: int
    status_id: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
