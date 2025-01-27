"""
Pydantic models for Nodes.
"""
from typing import Optional, Union
from pydantic import BaseModel

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
    id       : int
    name     : str
    children : Optional[Union[list["PydanticNodeModel"], list[int]]] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True


class PydanticUEInNodeModel(AcademicYearPydanticModel):
    """
    Pydantic model for a Node with its UEs.
    """
    id       : int
    type     : str

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True

class PydanticNodeFrontModel(AcademicYearPydanticModel):
    """
    Pydantic model for a Node with its UEs.
    """
    id       : int
    type     : str
    name     : str
    children : Optional[Union[list["PydanticNodeFrontModel"], list["PydanticUEInNodeModel"]]] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True
