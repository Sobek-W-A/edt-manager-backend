"""
This module contains the CourseTypeInDB model which is used to store
different types of courses.
"""
from tortoise.fields import CharField, Field, IntField, TextField

from app.models.tortoise.abstract.academic_year import AcademicYear


class CourseTypeInDB(AcademicYear):
    """
    This model represents a course type that can be assigned to a course.
    """
    id          : Field[int] = IntField(pk=True)
    name        : Field[str] = CharField(max_length=128)
    description : Field[str] = TextField()

    class Meta(AcademicYear.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "CourseType"

