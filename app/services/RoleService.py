"""
Role-related operations service.
Provides the methods to use when interacting with a role.
"""
from app.models.pydantic.RoleModel import PydanticRoleModel
from app.models.tortoise.role import RoleInDB


async def get_all_roles() -> list[PydanticRoleModel]:
    """
        This method retrieves all accounts.
    """

    roles : list[RoleInDB] = await RoleInDB.all()
    return [PydanticRoleModel.model_validate(role) for role in roles]

async def get_role_by_id(role_id: int) -> PydanticRoleModel:

    return await RoleInDB.get(role_id=role_id)


async def add_role(role: RoleInDB) -> PydanticRoleModel:

    return None
