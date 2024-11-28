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

    async def to_dict(self) -> dict:
        """
        Converts RoleInDB instance into a dictionary, including related permissions.
        """
        return {
            "role_name": self.role_name,
            "role_description": self.role_description,
            "permissions": [await permission.to_dict() for permission in await self.permissions.all()],
        }

    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "Role"