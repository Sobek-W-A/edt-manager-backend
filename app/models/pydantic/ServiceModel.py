"""
Pydantic models for services.
"""

from app.models.pydantic.abstract.ClassicModel import ClassicModel


class PydanticServiceModelFromJSON(ClassicModel):
    """
    Pydantic model for services. Used to load data from JSON files.
    """

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True

class PydanticServiceModel(ClassicModel):
    """
    Pydantic model for services.
    """

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True

class PydanticServiceExportModel(ClassicModel):
    """
    Pydantic model for exporting services to JSON.
    """

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True
