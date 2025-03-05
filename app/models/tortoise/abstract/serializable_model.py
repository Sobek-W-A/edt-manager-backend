"""
Provides the abstract class SerializableModel.
This class is used to export or import the database model in JSON format.
"""
from typing import Any
from pydantic import BaseModel
from tortoise.models import Model
from tortoise.fields import Field
from tortoise.fields.relational import ManyToManyFieldInstance

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
        m2m_fields: list[str] = []
        fields: dict[str, Field[Any]] = cls._meta.fields_map    # type: ignore
        for field_name, field in fields.items():
            if isinstance(field, ManyToManyFieldInstance):
                m2m_fields.append(field_name)

        print(str(model.__name__) + " -> M2M's = " + str(m2m_fields))

        # Fetch objects with related Many-to-Many fields
        objects = await cls.all().prefetch_related(*m2m_fields)

        # Convert to Pydantic models
        return [model.model_validate(obj) for obj in objects]
