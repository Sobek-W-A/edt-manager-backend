"""
This module provides the RolePydanticModel class.
"""
from typing import Optional

from pydantic import BaseModel

from app.models.pydantic.PermissionsModel import PydanticPermissionsModel


class PydanticRoleModel(BaseModel):

    role_id: int
    name: str
    description: str
    permission_id: PydanticPermissionsModel

class PydanticCreateRoleModel(BaseModel):

    name: str
    description: str
    permission_id: Optional [PydanticPermissionsModel]

