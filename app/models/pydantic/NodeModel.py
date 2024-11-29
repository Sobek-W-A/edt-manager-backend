"""
Pydantic models for Nodes.
"""
from pydantic import BaseModel


class PydanticNodeModelFromJSON(BaseModel):
    """
    Model for Nodes loaded from JSON files.
    """
    name          : str
    parent_id     : int | None
    academic_year : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True
