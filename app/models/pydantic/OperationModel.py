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
