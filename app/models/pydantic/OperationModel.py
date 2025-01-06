"""
Pydantic models for Operations.
"""
from app.models.pydantic.abstract.ClassicModel import ClassicModel

class PydanticOperationModelFromJSON(ClassicModel):
    """
    This model is used to import JSON Operations into the database.
    """

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticOperationModel(ClassicModel):
    """
    Pydantic model for Operations.
    """

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True
