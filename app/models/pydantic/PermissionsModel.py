"""
Pydantic Permission Models.
"""

from pydantic import BaseModel

from app.models.pydantic.OperationModel import PydanticOperationModel
from app.models.pydantic.ServiceModel import PydanticServiceModel


class PydanticPermissionsModel(BaseModel):
    """
    Pydantic model for permissions used to send Permissions to the Frontend.
    """
    id          : int
    service     : PydanticServiceModel   | int
    operation   : PydanticOperationModel | int

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True

class PydanticPermissionModelFromJSON(BaseModel):
    """
    Pydantic model for permissions. Used to load data from JSON files.
    """
    service_name_id    : str
    operation_name_id  : str

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True

class PydanticPermissionExportModel(BaseModel):
    """
    Pydantic model for exporting permissions to JSON.
    """
    id            : int
    service_id  : str
    operation_id: str

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True
