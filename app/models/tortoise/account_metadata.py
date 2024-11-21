"""
This file contains the AccountMetadata class, which is a M2M relation that links accounts and permissions by Academic years.
"""

from tortoise import Model
from tortoise.fields import ForeignKeyField, ForeignKeyRelation, IntField, Field

from app.models.tortoise.account import AccountInDB
from app.models.tortoise.role import RoleInDB


class AccountMetadata(Model):
    """
    This class is a M2M relation that links accounts and permissions by Academic years.
    """
    account       : ForeignKeyRelation[AccountInDB] = ForeignKeyField("models.AccountInDB", related_name="metadata")
    role          : ForeignKeyRelation[RoleInDB]    = ForeignKeyField("models.RoleInDB", related_name="metadata")
    academic_year : Field[int]                      = IntField(required=True)
    
    class Meta: # type: ignore
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "AccountMetadata"
