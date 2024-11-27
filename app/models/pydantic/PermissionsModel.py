"""
This module provides the PermissionsPydanticModel class.
"""
from pydantic import BaseModel

from app.models.pydantic.OperationModel import PydanticOperationModel
from app.models.pydantic.ServiceModel import PydanticServiceModel


class PydanticPermissionsModel(BaseModel):

    permission_id: int
    service_id: PydanticServiceModel
    operation_id: PydanticOperationModel


