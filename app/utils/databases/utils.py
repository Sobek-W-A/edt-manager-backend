"""
This module regroups utility functions that does not fit anywhere else.
"""


from typing import Any

from tortoise import Model


def get_fields_from_model(model: type[Model]) -> dict[str, Any]:
    """
    This function retrieves the fields from a Tortoise model.

    Args:
        model (Model): The Tortoise model to retrieve the fields from.

    Returns:
        dict[str, Field]: The fields of the Tortoise model.
    """
    # We need to type ignore there, no other choice.
    return model._meta.fields_map.keys() # pylint: disable=protected-access # type: ignore
