"""
This module provides the Account model to the API.
It is used to handle auth related operation and separate user information from auth information.
"""

from typing import TYPE_CHECKING

from tortoise.fields import (CharField, Field, IntField,
                             ForeignKeyNullableRelation, TextField)

from app.models.tortoise.abstract.serializable_model import SerializableModel

if TYPE_CHECKING:
    from app.models.tortoise.profile import ProfileInDB

class AccountInDB(SerializableModel):
    """
    This class is the tortoise model for authentication.
    Will probably be removed in the future when UL auth will be used.
    """
    id      : Field[int] = IntField(primary_key=True)
    login   : Field[str] = CharField(unique=True, required=True, max_length=128)
    hash    : Field[str] = TextField(required=True)

    profile : ForeignKeyNullableRelation["ProfileInDB"]

    def __str__(self) -> str:
        """
        This method will output a str describing the Account class.
        """
        return f"[INFO] - ACCOUNT {self.login} ID : {self.id}"

    class Meta(SerializableModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table   : str = "Account"
        abstract: bool = False
