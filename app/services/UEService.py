"""
UE-related operations service.
Provides the methods to use when interacting with an UE.
"""

from app.models.pydantic.UEModel import PydanticUEModel
from app.models.tortoise.role import RoleInDB


async def get_ue_by_id(role_id: int) -> PydanticUEModel:

    return await RoleInDB.get(role_id=role_id)


async def add_ue() -> PydanticUEModel:

    return None
