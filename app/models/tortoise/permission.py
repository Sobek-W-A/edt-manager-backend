"""
Database object representing a permission that can be granted to a user.
"""
from tortoise.models import Model
from tortoise import fields

class Permission(Model):
    """
    This model represents a permission that can be granted to a user.
    """
    id              = fields.IntField(pk=True)
    service_id      = fields.ForeignKeyField("models.Service",   related_name="service")   # type: ignore
    operation_id    = fields.ForeignKeyField("models.Operation", related_name="operation")   # type: ignore
