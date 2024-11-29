"""
This module provides the RolePydanticModel class.
"""
from typing import Optional, List

from pydantic import BaseModel

from app.models.pydantic.abstract.ClassicModel import ClassicModel
from app.models.pydantic.PermissionsModel import PydanticPermissionsModel

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
