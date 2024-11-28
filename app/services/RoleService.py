"""
Role-related operations service.
Provides the methods to use when interacting with a role.
"""
from fastapi import HTTPException

from app.models.pydantic.RoleModel import PydanticRoleModel
from app.models.tortoise.role import RoleInDB
from app.utils.enums.http_errors import CommonErrorMessages


async def get_all_roles() -> list[PydanticRoleModel]:
    """
        This method retrieves all roles.
    """

    roles : list[RoleInDB] = await RoleInDB.all()
    return [PydanticRoleModel.model_validate(role) for role in roles]

async def get_role_by_id(role_id: int) -> PydanticRoleModel:
    """
        This method retrieves a role .
    """
    role: RoleInDB | None = await RoleInDB.get_or_none(id=role_id)

    if role is None:
        raise HTTPException(status_code=404,detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    return PydanticRoleModel.model_validate(role)


async def add_role(role: RoleInDB) -> PydanticRoleModel:

    return None


async def modify_role(role_id, body) -> None :

    return None


async def delete_role(role_id) -> None:
    role: RoleInDB | None = await RoleInDB.get_or_none(id=role_id)

    if role is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    await role.delete()