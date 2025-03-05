"""
This module represents the role model that can be granted to a user.
A role grants several permissions to the user.
"""
from tortoise.fields import ManyToManyField, ManyToManyRelation

from app.models.tortoise.abstract.classic_model import ClassicModel
from app.models.tortoise.permission import PermissionInDB


class RoleInDB(ClassicModel):
    """
    This model represents a role that can be granted to a user.
    """
    permissions : ManyToManyRelation[PermissionInDB] = ManyToManyField("models.PermissionInDB", related_name="permission")

    class Meta(ClassicModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "Role"
