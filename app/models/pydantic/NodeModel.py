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
    parent_id     : int  | None
    academic_year : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True


class PydanticNodeModelWithChildIds(AcademicYearPydanticModel):
    """
    This module provides a model for a Folder.
    """
    id         : int
    name       : str
    type       : str = "node"
    child_nodes: Optional[list[Union[int, "PydanticUEInNodeModel"]]] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True
        from_attributes: bool = True


class PydanticNodeModel(AcademicYearPydanticModel):
    """
    This module provides a model for a Folder.
    """
    id         : int
    name       : str
    type       : str = "node"
    child_nodes: Optional[Union[list["PydanticUEInNodeModel"], list["PydanticNodeModel"]]] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True
        from_attributes: bool = True

class PydanticUEInNodeModel(PydanticNodeModel):
    """
    Pydantic model for a Node with its UEs.
    """
    id  : int
    name: str
    type: str = "ue"


class PydanticNodeCreateModel(BaseModel):
    """
    Pydantic model for creating a Node.
    """
    name         : str
    parent_id    : Optional[int] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True

class PydanticNodeUpdateModel(BaseModel):
    """
    Pydantic model for creating a Node.
    """
    name         : Optional[str] = None
    parent_id    : Optional[int] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True

class PydanticNodeFrontModel(AcademicYearPydanticModel):
    """
    Pydantic model for a Node with its UEs.
    """
    id         : int
    name       : str
    child_nodes: Optional[Union[list["PydanticNodeFrontModel"], list["PydanticUEInNodeModel"]]] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True
