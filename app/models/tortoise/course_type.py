"""
This module contains the CourseTypeInDB model which is used to store
different types of courses.
"""
from tortoise import Model
from tortoise.fields import CharField, Field, IntField, TextField

class CourseTypeInDB(Model):
    """
    This model represents a course type that can be assigned to a course.
    """
    id          : Field[int] = IntField(pk=True)
    name        : Field[str] = CharField(max_length=128)
    description : Field[str] = TextField()

    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "CourseType"

