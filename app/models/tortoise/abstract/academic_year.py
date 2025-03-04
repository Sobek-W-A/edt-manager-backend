"""
Provides an abstract models to make easier the creation of tables that needs an academic year.
"""
from tortoise.fields import Field, IntField

from app.models.tortoise.abstract.serializable_model import SerializableModel


class AcademicYear(SerializableModel):
    """
    This class is meant to be used with all tables that needs an academic year.
    A.K.A : Almost all of them.
    It inherits from Model, so no need to specify it again inside your child model.
    """
    academic_year : Field[int] = IntField(required=True, default=2024)

    class Meta(SerializableModel.Meta):
        """
        This class specifies that our schema is abstract.
        """
        abstract: bool = True
