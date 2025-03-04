"""
Pydantic models for the AccountMetadata model.
"""
from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel


class PydanticAccountMetaModelFromJSON(AcademicYearPydanticModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    account_id    : int
    role_id       : str

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticAccountMetaExportModel(AcademicYearPydanticModel):
    """
    Pydantic Model for AccountMetadata. This model is used to validate and transform JSON data.
    """
    account_id    : int
    role_id       : str

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
