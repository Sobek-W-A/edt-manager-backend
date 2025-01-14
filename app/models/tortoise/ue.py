"""
This module contains the model for the UE.
"""
from tortoise.fields import ManyToManyField, ManyToManyRelation, ForeignKeyNullableRelation, ForeignKeyField

from app.models.pydantic.CourseModel import PydanticCourseModel
from app.models.pydantic.UEModel import PydanticUEModel
from app.models.tortoise.course import CourseInDB
from app.models.tortoise.node import NodeInDB

class UEInDB(NodeInDB):
    """
    This model represents a UE.
    """
    # Override `parent` to remove backward relation duplication
    parent: ForeignKeyNullableRelation["NodeInDB"] = ForeignKeyField(
        "models.NodeInDB",
        related_name=None,  # Disable backward relation for this subclass
        null=True,
    )

    courses : ManyToManyRelation[CourseInDB] = ManyToManyField("models.CourseInDB",
                                                               related_name="ue",
                                                               through="ue_courses")

    class Meta(NodeInDB.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table : str = "UE"

    async def to_pydantic(self) -> "PydanticUEModel":
        """
        Convert this UE instance to a Pydantic model.
        """
        # Charger toutes les courses associées à cette UE
        related_courses = await self.courses.all()

        # Transformer les courses en modèles Pydantic
        return PydanticUEModel(
            academic_year=self.academic_year,
            ue_id=self.id,
            name=self.name,
            courses=[PydanticCourseModel(**course.__dict__) for course in related_courses],
        )

