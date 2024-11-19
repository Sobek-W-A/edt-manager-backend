"""
This module is made to provide different user models to the API.
It contains pydantic and Tortoise models.
"""
from tortoise.fields import (Field,
                             IntField,
                             ForeignKeyRelation,
                             CharField,
                             ForeignKeyField)
from tortoise.models import Model

from app.models.tortoise.account import AccountInDB
from app.models.tortoise.role import RoleInDB
from app.utils.enums.permission_enums import AvailableRoles


class UserInDB(Model):
    """
    This class is designed to design the table inside of the database.
    It contains all the columns necessary to store the user.
    """
    id        : Field[int]                      = IntField(primary_key=True)
    firstname : Field[str]                      = CharField(max_length=128)
    lastname  : Field[str]                      = CharField(max_length=128)
    mail      : Field[str]                      = CharField(unique=True, required=True, max_length=128)
    role      : ForeignKeyRelation[RoleInDB]    = ForeignKeyField("models.RoleInDB", related_name="role", default=AvailableRoles.ADMIN.value.role_name)
    account   : ForeignKeyRelation[AccountInDB] = ForeignKeyField("models.AccountInDB", related_name="account", default=None)

    def __str__(self) -> str:
        """
        This method will output a str describing the UserInDB class.
        """
        return f"[INFO] - USER {self.firstname} {self.lastname} ID : {self.id}"

    class Meta: # type: ignore
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "User"
