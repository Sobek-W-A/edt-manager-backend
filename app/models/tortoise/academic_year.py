"""
Provides an abstract models to make easier the creation of tables that needs an academic year.
"""

from tortoise import Model
from tortoise.fields import Field, IntField


class AcademicYear(Model):
    """
    This class is meant to be used with all tables that needs an academic year.
    A.K.A : Almost all of them.
    It inherits from Model, so no need to specify it again inside your child model.
    """
    academic_year : Field[int] = IntField(required=True, default=2024)

    class Meta(Model.Meta):
        """
        This class specifies that our schema is abstract.
        """
        abstract = True
