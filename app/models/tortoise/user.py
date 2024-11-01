"""
This module is made to provide different user models to the API.
It contains pydantic and Tortoise models.
"""

from tortoise.fields import Field, IntField, ForeignKeyRelation, CharField, TextField, ForeignKeyField
from tortoise.models import Model

from app.models.tortoise.role import RoleInDB



class UserInDB(Model):
    """
    This class is designed to design the table inside of the database.
    It contains all the columns necessary to store the user.
    """
    id        : Field[int]                   = IntField(primary_key=True)
    login     : Field[str]                   = CharField(unique=True, required=True, max_length=128)
    firstname : Field[str]                   = CharField(max_length=128)
    lastname  : Field[str]                   = CharField(max_length=128)
    mail      : Field[str]                   = CharField(unique=True, required=True, max_length=128)
    hash      : Field[str]                   = TextField(required=True)
    role      : ForeignKeyRelation[RoleInDB] = ForeignKeyField("models.RoleInDB", related_name="role")

    def __str__(self) -> str:
        """
        This method will output a str describing the UserInDB class.
        """
        return f"[INFO] - USER {self.login} ID : {self.id}"

    class Meta: # type: ignore
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "User"
