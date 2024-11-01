"""
This module describes the operations.
These are basically CRUD actions that can be performed on a service.
"""
from tortoise.models import Model
from tortoise import fields


class OperationInDB(Model):
    """
    This class regroups the CRUD operations that can be performed on a service.
    Mainly used for permissions.
    """
    operation_name          = fields.CharField(max_length=128, pk=True)
    operation_description   = fields.TextField()

    class Meta: # type: ignore
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "Operation"
