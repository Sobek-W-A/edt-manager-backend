"""
This module describes the operations.
These are basically CRUD actions that can be performed on a service.
"""
from tortoise.models import Model
from tortoise.fields import Field, CharField, TextField


class OperationInDB(Model):
    """
    This class regroups the CRUD operations that can be performed on a service.
    Mainly used for permissions.
    """
    operation_name        : Field[str] = CharField(max_length=128, pk=True)
    operation_description : Field[str] = TextField()

    def to_dict(self) -> dict:
        """
        Convert the OperationInDB instance to a dictionary.
        """
        return {
            "operation_name": self.operation_name,
            "operation_description": self.operation_description
        }

    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "Operation"
