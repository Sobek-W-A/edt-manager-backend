"""
This module describes the services.
These are basically the services (routes) that can be provided to a user.
"""
from tortoise.models import Model
from tortoise.fields import Field, CharField, TextField


class ServiceInDB(Model):
    """
    This model represents a service that can be provided to a user.
    It is mainly used for permissions.
    """
    service_name        : Field[str] = CharField(max_length=128, pk=True)
    service_description : Field[str] = TextField()

    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "Service"
