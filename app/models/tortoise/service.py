from tortoise.models import Model
from tortoise import fields


class Service(Model):
    """
    This model represents a service that can be provided to a user.
    It is mainly used for permissions.
    """
    id = fields.IntField(pk=True)
    service_name = fields.CharField(max_length=128)
    service_description = fields.TextField()
