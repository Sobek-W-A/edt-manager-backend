"""
Pydantic models for Nodes.
"""
from typing import List, Optional
from pydantic import BaseModel

from app.models.pydantic.UEModel import PydanticUEModel
from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel


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


class PydanticNodeModel(AcademicYearPydanticModel):
    """
    This module provides a model for a Folder.
    """
    name     : str
    children : Optional[List["PydanticNodeModel"]] = None
    ue       : Optional[PydanticUEModel] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True
