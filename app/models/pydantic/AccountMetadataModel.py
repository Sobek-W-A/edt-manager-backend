"""
Pydantic models for the AccountMetadata model.
"""
from pydantic import BaseModel


class PydanticAccountMetaModelFromJSON(BaseModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    account_id    : int
    role_id       : str
    academic_year : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
