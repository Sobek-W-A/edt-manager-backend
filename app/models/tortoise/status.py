"""
This module describes statuses that can be assigned to profiles.
These are used to determine the coefficients that needs to be applied
when we need to calculate the total of hours dispensed.
"""

from tortoise.fields import Field, IntField, CharField, TextField
from app.models.tortoise.abstract.academic_year import AcademicYear

class StatusInDB(AcademicYear):
    """
    This model represents a status that can be assigned to a profile.
    """
    id          : Field[int] = IntField(pk=True)
    name        : Field[str] = CharField(max_length=128)
    description : Field[str] = TextField()
    quota       : Field[int] = IntField(min_size=0, default=0)

    class Meta(AcademicYear.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table    : str = "Status"
        abstract : bool = False
