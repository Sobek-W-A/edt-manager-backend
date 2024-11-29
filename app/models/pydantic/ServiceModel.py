"""
Pydantic models for services.
"""

from pydantic import BaseModel


class PydanticServiceModelFromJSON(BaseModel):
    """
    Pydantic model for services. Used to load data from JSON files.
    """
    name : str
    description : str

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes = True
