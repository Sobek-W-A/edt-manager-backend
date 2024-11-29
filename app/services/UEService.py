"""
UE-related operations service.
Provides the methods to use when interacting with an UE.
"""
from fastapi import HTTPException

from app.models.pydantic.UEModel import PydanticUEModel
from app.models.tortoise.role import RoleInDB
from app.utils.enums.http_errors import CommonErrorMessages


async def get_ue_by_id(ue_id: int) -> PydanticUEModel:

    return await RoleInDB.get(role_id=ue_id)


async def add_ue() -> PydanticUEModel:

    return None



async def modify_ue(ue_id, body):
    return None


async def delete_ue(ue_id) -> None:


    return None