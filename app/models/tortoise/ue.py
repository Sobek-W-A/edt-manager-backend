"""
This module contains the model for the UE.
"""
from tortoise.fields import (ManyToManyField, ManyToManyRelation,
                             ForeignKeyNullableRelation)

from app.models.tortoise.course import CourseInDB
from app.models.tortoise.node import NodeInDB

class UEInDB(NodeInDB):
    """
    This model represents a UE.
    """
    # Override `parent` and child_nodes to remove backward relation duplication
    parent: ManyToManyRelation[NodeInDB] = ManyToManyField(         # type: ignore
        "models.NodeInDB",
        related_name="ues",
        through="UE_NODE_ASSOCIATION"
    )
    child_nodes: ForeignKeyNullableRelation["NodeInDB"] = None

    courses : ManyToManyRelation[CourseInDB] = ManyToManyField("models.CourseInDB",
                                                               related_name="ue",
                                                               through="UE_COURSES_ASSOCIATION")

    class Meta(NodeInDB.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "UE"
