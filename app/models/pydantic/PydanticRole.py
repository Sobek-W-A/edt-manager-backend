"""
Pydantic Models for Roles.
"""
from typing import List, Optional

from pydantic import BaseModel

from app.models.pydantic.PermissionsModel import PydanticPermissionsModel
from app.models.pydantic.abstract.ClassicModel import ClassicModel


class PydanticRoleModelFromJSON(BaseModel):
    """
    Pydantic Model for Role. This model is used to validate and transform JSON data.
    """
    name: str
    description: str
    permissions_m2m: list[int]

    class Config:
        """
        Pydantic configuration for Role.
        """
        from_attributes : bool = True

class PydanticRoleModel(ClassicModel):
    """
    Pydantic Model for Role. This model is a role.
    """
    permissions: List[PydanticPermissionsModel]

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes: bool = True

class PydanticCreateRoleModel(ClassicModel):
    """
    Pydantic Model for Role. This model is used to create a role.
    """
    permissions: Optional[List[int]]

class PydanticUpdateRoleModel(ClassicModel):
    """
    Pydantic Model for Role. This model is used to update a role.
    """
    permissions: Optional[List[int]]

class PydanticRoleResponseModel(ClassicModel):
    """
    Pydantic Model for Role. This model is used to get a role.
    """

class PydanticSetRoleToAccountModel(BaseModel):
    """
    Pydantic Model for Role. This model is used to set a role to an account.
    """
    name          : str
    academic_year : int
