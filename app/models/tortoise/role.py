"""
This module represents the role model that can be granted to a user.
A role grants several permissions to the user.
"""
from tortoise.models import Model
from tortoise.fields import Field, CharField, TextField, ManyToManyField, ManyToManyRelation

from app.models.tortoise.permission import PermissionInDB
from models.tortoise.abstract.classic_model import ClassicModel


class RoleInDB(ClassicModel):
    """
    This model represents a role that can be granted to a user.
    """
    permissions : ManyToManyRelation[PermissionInDB] = ManyToManyField("models.PermissionInDB", related_name="permission")

    class Meta(ClassicModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "Role"
