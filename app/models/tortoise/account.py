"""
This module provides the Account model to the API.
It is used to handle auth related operation and separate user information from auth information.
"""

from tortoise.fields import Field, IntField, TextField, CharField
from tortoise.models import Model

class AccountInDB(Model):
    """
    This class is the tortoise model for authentication.
    Will probably be removed in the future when UL auth will be used.
    """
    id      : Field[int] = IntField(primary_key=True)
    login   : Field[str] = CharField(unique=True, required=True, max_length=128)
    hash    : Field[str] = TextField(required=True)

    def __str__(self) -> str:
        """
        This method will output a str describing the Account class.
        """
        return f"[INFO] - ACCOUNT {self.login} ID : {self.id}"

    class Meta(Model.Meta):
        """a
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "Account"
