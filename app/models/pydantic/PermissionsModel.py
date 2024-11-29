"""
Pydantic Permission Models.
"""

from pydantic import BaseModel

from app.models.pydantic.ClassicModel import ClassicModel


class PydanticPermissionsModel(BaseModel):
    """
    Pydantic model for permissions used to send Permissions to the Frontend.
    """
    id: int
    service_name: ClassicModel
    operation_name: ClassicModel

    class Config:
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