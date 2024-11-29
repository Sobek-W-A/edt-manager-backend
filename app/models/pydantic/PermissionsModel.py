"""
This module provides the PermissionsPydanticModel class.
"""
from pydantic import BaseModel

from app.models.pydantic.ClassicModel import ClassicModel


class PydanticPermissionsModel(BaseModel):

    id: int
    service_name: ClassicModel
    operation_name: ClassicModel

    class Config:
        from_attributes = True
