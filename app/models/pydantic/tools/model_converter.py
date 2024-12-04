"""
This module provides a function to convert a Tortoise model to a Pydantic model.
"""

from typing import Any, Optional, Type

from pydantic import BaseModel
from tortoise import Model

async def tortoise_to_pydantic(
    tortoise_obj: Type[Model],
    pydantic_model: Type[BaseModel],
    related_pydantic_models: Optional[dict[str, Type[BaseModel]]] = None
) -> BaseModel:
    """
    Converts a Tortoise model instance to a Pydantic model instance.
    It can import 1-deep foreign relation in the pydantic model.
    You will still need to make sure the pydantic model is properly defined, with a field that
    is either an int or the foreign pydantic model.

    :param tortoise_obj: Instance of a Tortoise model.
    :param pydantic_model: Pydantic model class corresponding to the Tortoise model.
    :param related_pydantic_models: Optional mapping of related field names to their Pydantic model classes.
    :return: An instance of the specified Pydantic model.
    """
    if related_pydantic_models is None:
        related_pydantic_models = {}

    # Extract the data from the Tortoise model
    data: dict[str, Any] = tortoise_obj.__dict__["_data"]

    for related_field, related_model in related_pydantic_models.items():
        related_instance = getattr(tortoise_obj, related_field, None)

        if related_instance and not isinstance(related_instance, int):
            # Prefetched relation; recursively convert it
            data[related_field] = await tortoise_to_pydantic(related_instance, related_model)
        else:
            # Relation not prefetched; include only the foreign key
            data[related_field] = data.get(f"{related_field}_id")

    # Return an instance of the Pydantic model
    return pydantic_model(**data)
