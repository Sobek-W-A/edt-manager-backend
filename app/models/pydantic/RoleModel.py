"""
This module provides the RolePydanticModel class.
"""
from typing import Optional, List

from pydantic import BaseModel

from app.models.pydantic.PermissionsModel import PydanticPermissionsModel


class PydanticRoleModel(BaseModel):

    name: str
    description: str
    permission_id: List[PydanticPermissionsModel]

class PydanticCreateRoleModel(BaseModel):

    name: str
    description: str
    permission_id: Optional[List[PydanticPermissionsModel]]

