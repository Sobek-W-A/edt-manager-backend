from tortoise.models import Model
from tortoise import fields


class Operation(Model):
    """
    This class regroups the CRUD operations that can be performed on a service.
    Mainly used for permissions.
    """
    id = fields.IntField(pk=True)
    operation_name = fields.CharField(max_length=128)
    operation_description = fields.TextField()
