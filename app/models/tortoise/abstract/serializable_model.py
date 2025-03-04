from pydantic import BaseModel
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator # type: ignore


class SerializableModel(Model):
    
    class Meta(Model.Meta):
        abstract = True

    @classmethod
    async def export[T: BaseModel](cls, model: T) -> list[T]:
        """
        Export du modèle en JSON
        """
        objects = await cls.all()
        return [model.model_validate(obj) for obj in objects]
        
