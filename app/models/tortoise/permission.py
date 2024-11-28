"""
Database object representing a permission that can be granted to a user.
"""
from tortoise.models import Model
from tortoise.fields import Field, IntField, ForeignKeyField, ForeignKeyRelation, CharField

from app.models.tortoise.service import ServiceInDB
from app.models.tortoise.operation import OperationInDB

class PermissionInDB(Model):
    """
    This model represents a permission that can be granted to a user.
    """
    id             : Field[int]                        = IntField(pk=True)
    service_name   : ForeignKeyRelation[ServiceInDB]   = ForeignKeyField("models.ServiceInDB",   related_name="service")
    operation_name : ForeignKeyRelation[OperationInDB] = ForeignKeyField("models.OperationInDB", related_name="operation")

    async def to_dict(self) -> dict:
        """
        Convert into dict
        """


        return {
            "permission_id": self.id,
            "service_name": self.service_name,
            "operation_name": self.operation_name
        }


    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "Permission"


