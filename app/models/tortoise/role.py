"""
This module represents the role model that can be granted to a user.
A role grants several permissions to the user.
"""
from tortoise.models import Model
from tortoise.fields import Field, CharField, TextField, ManyToManyField, ManyToManyRelation

from app.models.tortoise.permission import PermissionInDB


class RoleInDB(Model):
    """
    This model represents a role that can be granted to a user.
    """
    role_name        : Field[str]                         = CharField(max_length=128, pk=True)
    role_description : Field[str]                         = TextField()
    permissions      : ManyToManyRelation[PermissionInDB] = ManyToManyField("models.PermissionInDB", related_name="permission")

    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "Role"
