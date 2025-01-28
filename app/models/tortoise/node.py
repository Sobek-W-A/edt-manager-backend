"""
This module contains the definition of the Composite model.

"""

from tortoise.fields import (CharField,
                             BooleanField,
                             IntField,
                             Field,
                             ForeignKeyField,
                             ForeignKeyNullableRelation)

from app.models.tortoise.abstract.academic_year import AcademicYear


class NodeInDB(AcademicYear):
    """
    This model represents a composite pattern.
    """

    id     : Field[int]  = IntField(pk=True)
    name   : Field[str]  = CharField(max_length=128)
    is_root: Field[bool] = BooleanField(default=False)

    parent : ForeignKeyNullableRelation["NodeInDB"] = ForeignKeyField("models.NodeInDB",
                                                                      related_name="child_nodes",
                                                                      null=True)
    child_nodes: ForeignKeyNullableRelation["NodeInDB"]

    class Meta(AcademicYear.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "Node"
