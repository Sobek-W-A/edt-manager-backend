"""
This module describes the operations.
These are basically CRUD actions that can be performed on a service.
"""
from app.models.tortoise.abstract.classic_model import ClassicModel


class OperationInDB(ClassicModel):
    """
    This class regroups the CRUD operations that can be performed on a service.
    Mainly used for permissions.
    """

    class Meta(ClassicModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str = "Operation"
