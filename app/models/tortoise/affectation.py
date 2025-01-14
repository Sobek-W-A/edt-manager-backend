"""
This module contains the AffectationInDB model which is used to represent the affectation of a course to a teacher.
"""

from datetime import datetime
from tortoise import Model
from tortoise.fields import (ForeignKeyField,
                             ForeignKeyRelation,
                             IntField,
                             Field,
                             CharField,
                             DatetimeField)

from app.models.tortoise.course import CourseInDB
from app.models.tortoise.profile import ProfileInDB


class AffectationInDB(Model):
    """
    This model represents the affectation of a course to a teacher.
    """

    id    : Field[int]      = IntField(pk=True)
    hours : Field[int]      = IntField(min_value=0)
    notes : Field[str]      = CharField(max_length=512, null=True)
    date  : Field[datetime] = DatetimeField(default=datetime.now)
    group : Field[int]      = IntField(min_value=1, default=1)

    course : ForeignKeyRelation[CourseInDB]  = ForeignKeyField("models.CourseInDB", related_name="affectation")
    profile: ForeignKeyRelation[ProfileInDB] = ForeignKeyField("models.ProfileInDB", related_name="affectation")

    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "Affectation"
