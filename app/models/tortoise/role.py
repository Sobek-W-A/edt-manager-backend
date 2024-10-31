from tortoise.models import Model
from tortoise import fields


class Role(Model):
    """
    This model represents a role that can be granted to a user.
    """
    id                  = fields.IntField(pk=True)
    role_name           = fields.CharField(max_length=128)
    role_description    = fields.TextField()
    permissions         = fields.ManyToManyField("app.models.tortoise.Permission", related_name="roles")
