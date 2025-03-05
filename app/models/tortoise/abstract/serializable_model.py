"""
Provides the abstract class SerializableModel.
This class is used to export or import the database model in JSON format.
"""
from pydantic import BaseModel
from tortoise.models import Model
from tortoise.fields import ManyToManyRelation

class SerializableModel(Model):
    """
    This class is used to export or import the model in JSON format.
    """

    class Meta(Model.Meta):
        """
        This class is used to indicate that the Table is abstract.
        """
        abstract: bool = True

    @classmethod
    async def export[T: BaseModel](cls, model: type[T]) -> list[T]:
        """
        Export du modèle en JSON.
        """
        # Get all fields that are relations (M2M or FK)
        # Detect Many-to-Many (M2M) fields
        m2m_fields = [
            field for field, attr in cls._meta.fields_map.items()
            if isinstance(getattr(cls, field), ManyToManyRelation)
        ]

        # Fetch objects with related Many-to-Many fields
        objects = await cls.all().prefetch_related(*m2m_fields)

        # Convert to Pydantic models
        return [model.model_validate(obj) for obj in objects]
