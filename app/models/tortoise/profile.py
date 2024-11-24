"""
This module is made to provide different user models to the API.
It contains pydantic and Tortoise models.
"""
from tortoise.fields import (Field,
                             IntField,
                             CharField,
                             ForeignKeyField,
                             ForeignKeyNullableRelation,
                             ForeignKeyRelation)

from app.models.tortoise.abstract.academic_year import AcademicYear
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.status import StatusInDB


class ProfileInDB(AcademicYear):
    """
    This class is designed to design the table inside of the database.
    It contains all the columns necessary to store the user.
    """
    id            : Field[int] = IntField(primary_key=True)
    firstname     : Field[str] = CharField(max_length=128)
    lastname      : Field[str] = CharField(max_length=128)
    mail          : Field[str] = CharField(unique=True, required=True, max_length=128)
    hours_to_work : Field[int] = IntField(min_value=0)

    account : ForeignKeyNullableRelation[AccountInDB] = ForeignKeyField("models.AccountInDB", related_name="profile", null=True)
    status  : ForeignKeyRelation[StatusInDB]          = ForeignKeyField("models.StatusInDB", related_name="profile")

    def __str__(self) -> str:
        """
        This method will output a str describing the UserInDB class.
        """
        return f"[INFO] - USER {self.firstname} {self.lastname} ID : {self.id}"

    class Meta(AcademicYear.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table    : str  = "Profile"
        abstract : bool = False
