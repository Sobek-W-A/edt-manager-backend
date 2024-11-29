"""
This module provides the RolePydanticModel class.
"""
from typing import Optional, List

from pydantic import BaseModel

from app.models.pydantic.ClassicModel import ClassicModel
from app.models.pydantic.PermissionsModel import PydanticPermissionsModel


class PydanticRoleModel(ClassicModel):

    permissions: List[PydanticPermissionsModel]

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes: bool = True




class PydanticCreateRoleModel(ClassicModel):

    permissions: Optional[List[int]]






