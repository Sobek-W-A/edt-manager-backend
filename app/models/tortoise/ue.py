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
        related_courses = await self.courses.all().prefetch_related("course_type")
        try:

            courses = [
                PydanticCourseModel(
                    id=course.id,
                    duration=course.duration,
                    group_count=course.group_count,
                    course_type=course.course_type.to_pydantic(),
                )
                for course in related_courses
            ]
        except Exception as e:
            raise ValueError(f"Error while converting courses to Pydantic models: {str(e)}")

            # Retourner le modèle UE
        return PydanticUEModel(
            academic_year=self.academic_year,
            ue_id=self.id,
            name=self.name,
            courses=courses,
        )

