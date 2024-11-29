"""
This file contains the AccountMetadata class, which is a M2M relation that
links accounts and permissions by Academic years.
"""

from tortoise.fields import ForeignKeyField, ForeignKeyRelation
from app.models.tortoise.abstract.academic_year import AcademicYear
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.role import RoleInDB


class AccountMetadataInDB(AcademicYear):
    """
    This class is a M2M relation that links accounts and permissions by Academic years.
    """
    account : ForeignKeyRelation[AccountInDB] = ForeignKeyField("models.AccountInDB", related_name="metadata")
    role    : ForeignKeyRelation[RoleInDB]    = ForeignKeyField("models.RoleInDB", related_name="metadata", default=1)

    class Meta(AcademicYear.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "AccountMetadata"
        abstract: bool = False

