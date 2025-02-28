"""
This module contains the CourseInDB model which is used to represent a
course that can be assigned to a profile.
"""

from tortoise.fields import (Field,
                             ForeignKeyField,
                             ForeignKeyRelation,
                             IntField)

from app.models.tortoise.abstract.academic_year import AcademicYear
from app.models.tortoise.course_type import CourseTypeInDB


class CourseInDB(AcademicYear):
    """
    This model represents a course that can be assigned to a profile.
    """
    id          : Field[int] = IntField(pk=True)
    duration    : Field[int] = IntField(min_value=0)
    group_count : Field[int] = IntField(min_value=1, default=1)
    course_type : ForeignKeyRelation[CourseTypeInDB] = ForeignKeyField("models.CourseTypeInDB",
                                                                       related_name="course")

    class Meta(AcademicYear.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "Course"
