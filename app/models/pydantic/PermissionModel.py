"""
Pydantic Permission Model.
"""

from pydantic import BaseModel

from app.models.pydantic.OperationModel import PydanticOperationModel
from app.models.pydantic.ServiceModel import PydanticServiceModel

class PydanticPermissionModel(BaseModel):
    """
    Pydantic model for permissions used to send Permissions to the Frontend.
    """
    service    : PydanticServiceModel
    operations : list[PydanticOperationModel] | list[str]

    class Config:
        """
        Pydantic configuration for the model.
        """
        from_attributes : bool = True
