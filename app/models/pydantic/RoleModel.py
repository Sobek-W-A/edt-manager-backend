"""
This module provides the RolePydanticModel class.
"""
from typing import Optional, List

from pydantic import BaseModel

from app.models.pydantic.PermissionsModel import PydanticPermissionsModel


class PydanticRoleModel(BaseModel):

    role_name: str
    role_description: str
    permissions: List[PydanticPermissionsModel]

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes: bool = True



class PydanticCreateRoleModel(BaseModel):
    role_name: str
    role_description: str
    permissions: Optional[List[int]]



