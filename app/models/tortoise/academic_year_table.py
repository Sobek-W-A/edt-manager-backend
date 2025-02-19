"""
This module contains the AcademicYearTableInDB model which is used to represent the
academic year which exist.
"""
from dataclasses import fields

from tortoise.fields import Field, IntField, TextField

from app.models.tortoise.abstract.academic_year import AcademicYear


class AcademicYearTableInDB(AcademicYear):
    """
        This class is the tortoise model for academic year table.
    """
    id: int = IntField(pk=True)
    description: str = TextField(null=False)


    class Meta(AcademicYear.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract: bool = False
        table : str = "AcademicYear"