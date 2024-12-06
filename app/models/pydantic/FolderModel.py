"""
This module provides the FolderPydanticModel class.
"""
from typing import Optional, List

from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.UEModel import PydanticUEModel


class PydanticFolderModel(AcademicYearPydanticModel):
    """
    This module provides a model for a Folder.
    """
    name: str
    children: Optional[List["PydanticFolderModel"]] = None
    ue: Optional[PydanticUEModel] = None

    class Config:
        """
        Pydantic configuration.
        """
        arbitrary_types_allowed : bool = True




