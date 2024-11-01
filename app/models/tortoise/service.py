"""
This module describes the services.
These are basically the services (routes) that can be provided to a user.
"""
from tortoise.models import Model
from tortoise import fields


class ServiceInDB(Model):
    """
    This model represents a service that can be provided to a user.
    It is mainly used for permissions.
    """
    service_name        = fields.CharField(max_length=128, pk=True)
    service_description = fields.TextField()

    class Meta: # type: ignore
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "Service"
