"""
This module represents the role model that can be granted to a user.
A role grants several permissions to the user.
"""
from tortoise.models import Model
from tortoise import fields


class RoleInDB(Model):
    """
    This model represents a role that can be granted to a user.
    """
    role_name           = fields.CharField(max_length=128, pk=True)
    role_description    = fields.TextField()
    permissions         = fields.ManyToManyField("models.PermissionInDB", related_name="permission")

    class Meta: # type: ignore
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "Role"
