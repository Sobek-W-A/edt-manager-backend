"""
Database object representing a permission that can be granted to a user.
"""
from tortoise.fields import Field, IntField, ForeignKeyField, ForeignKeyRelation

from app.models.tortoise.abstract.serializable_model import SerializableModel
from app.models.tortoise.service import ServiceInDB
from app.models.tortoise.operation import OperationInDB

class PermissionInDB(SerializableModel):
    """
    This model represents a permission that can be granted to a user.
    """
    id        : Field[int]                        = IntField(pk=True)
    service   : ForeignKeyRelation[ServiceInDB]   = ForeignKeyField("models.ServiceInDB",   related_name="service")
    operation : ForeignKeyRelation[OperationInDB] = ForeignKeyField("models.OperationInDB", related_name="operation")


    class Meta(SerializableModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "Permission"
