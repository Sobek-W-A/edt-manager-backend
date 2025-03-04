"""
Pydantic Models for Roles.
"""
from typing import Optional

from pydantic import BaseModel

from app.models.pydantic.PermissionModel import PydanticPermissionModel
from app.models.pydantic.abstract.ClassicModel import ClassicModel


class PydanticRoleModel(ClassicModel):
    """
    Pydantic Model for Role.
    """
    permissions: list[PydanticPermissionModel]

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes: bool = True

class PydanticCreateRoleModel(ClassicModel):
    """
    Pydantic Model for Role. This model is used to create a role.
    """
    permissions: Optional[list[int]]

class PydanticUpdateRoleModel(ClassicModel):
    """
    Pydantic Model for Role. This model is used to update a role.
    """
    permissions: Optional[list[int]]

class PydanticRoleResponseModel(ClassicModel):
    """
    Pydantic Model for Role. This model is used to get a role.
    """
    permissions: list[PydanticPermissionModel] = []

class PydanticSetRoleToAccountModel(BaseModel):
    """
    Pydantic Model for Role. This model is used to set a role to an account.
    """
    name          : str
    academic_year : int
