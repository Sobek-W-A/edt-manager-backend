"""
This module represents the role model that can be granted to a user.
A role grants several permissions to the user.
"""
from tortoise.models import Model
from tortoise import fields


class Role(Model):
    """
    This model represents a role that can be granted to a user.
    """
    id                  = fields.IntField(pk=True)
    role_name           = fields.CharField(max_length=128)
    role_description    = fields.TextField()
    permissions         = fields.ManyToManyField("models.Permission", related_name="permission")
