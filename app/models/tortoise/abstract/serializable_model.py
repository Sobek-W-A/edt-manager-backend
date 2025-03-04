"""
Provides the abstract class SerializableModel.
This class is used to export or import the database model in JSON format.
"""
from pydantic import BaseModel
from tortoise.models import Model

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
    async def export[T: BaseModel](cls, model: T) -> list[T]:
        """
        Export du modèle en JSON
        """
        objects = await cls.all()
        return [model.model_validate(obj) for obj in objects]
