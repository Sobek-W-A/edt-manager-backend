"""
Pydantic models for Operations.
"""
from pydantic import BaseModel

class PydanticOperationModelFromJSON(BaseModel):
    """
    This model is used to import JSON Operations into the database.
    """
    name        : str
    description : str

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
