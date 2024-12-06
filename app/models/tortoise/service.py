"""
This module describes the services.
These are basically the services (routes) that can be provided to a user.
"""
from app.models.tortoise.abstract.classic_model import ClassicModel


class ServiceInDB(ClassicModel):
    """
    This model represents a service that can be provided to a user.
    It is mainly used for permissions.
    """

    class Meta(ClassicModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table    : str = "Service"
        abstract : bool = False
