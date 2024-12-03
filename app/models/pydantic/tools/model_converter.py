"""
This module provides a function to convert a Tortoise model to a Pydantic model.
"""

from typing import Any, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from tortoise import Model

TortoiseModelType = TypeVar("TortoiseModelType", bound=Model)
PydanticModelType = TypeVar("PydanticModelType", bound=BaseModel)

RecursiveDict = dict[str, Union[Type[BaseModel], "RecursiveDict"]]

async def tortoise_to_pydantic(
    tortoise_obj: Type[TortoiseModelType],
    pydantic_model: Type[PydanticModelType],
    related_pydantic_models: Optional[RecursiveDict] = None
) -> PydanticModelType:
    """
    Converts a Tortoise model to a Pydantic model.
    Includes data from related models if related_pydantic_models is provided.
    Args:
        tortoise_model (Type[Model]): The Tortoise model to convert.
        pydantic_model (Type[baseModel]): The Pydantic model to convert to.
        related_pydantic_models: Optional mapping of related field names to either a Pydantic model class (Type[BaseModel]) for direct mapping or a nested dictionary mapping for recursive relations.
    Returns:
        An instance of the specified Pydantic model, built recursively if needed.
    """
    if related_pydantic_models is None:
        related_pydantic_models = {}

    # Extract the data from the Tortoise model
    data: dict[str, Any] = tortoise_obj.__dict__["_data"]

    for related_field, relation_model in related_pydantic_models.items():
        related_instance = getattr(tortoise_obj, related_field, None)

        if related_instance and not isinstance(related_instance, int):
            if isinstance(relation_model, dict):
                # Nested relation
                nested_pydantic_model = relation_model.get("model")
                nested_relations = relation_model.get("relations", {})
                data[related_field] = await tortoise_to_pydantic(
                    related_instance,
                    nested_pydantic_model,
                    nested_relations
                )
            else:
                # Direct relation
                data[related_field] = await tortoise_to_pydantic(
                    related_instance,
                    relation_model
                )
        else:
            # Relation not prefetched; include only the foreign key
            data[related_field] = data.get(f"{related_field}_id")

    # Return an instance of the Pydantic model
    return pydantic_model(**data)
