"""
Database object representing a permission that can be granted to a user.
"""
from tortoise.models import Model
from tortoise import fields

class PermissionInDB(Model):
    """
    This model represents a permission that can be granted to a user.
    """
    id              = fields.IntField(pk=True)
    service_name    = fields.ForeignKeyField("models.ServiceInDB",   related_name="service")     # type: ignore
    operation_name  = fields.ForeignKeyField("models.OperationInDB", related_name="operation")   # type: ignore

    class Meta: # type: ignore
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "Permission"
