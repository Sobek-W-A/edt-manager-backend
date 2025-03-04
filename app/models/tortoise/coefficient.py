"""
This module contains the definition of the CoefficientInDB model.
"""
from tortoise.models import Model
from tortoise.fields import (Field,
                             FloatField,
                             ForeignKeyField,
                             ForeignKeyRelation)
from app.models.tortoise.course_type import CourseTypeInDB
from app.models.tortoise.status import StatusInDB


class CoefficientInDB(Model):
    """
    This model represents a coefficient that can be assigned to a course depending on a status.
    """
    multiplier: Field[float] = FloatField(min_value=0, default=1.0)

    course_type : ForeignKeyRelation[CourseTypeInDB] = ForeignKeyField("models.CourseTypeInDB", related_name="coefficient")
    status      : ForeignKeyRelation[StatusInDB]     = ForeignKeyField("models.StatusInDB", related_name="coefficient")

    class Meta(Model.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "Coefficient"
