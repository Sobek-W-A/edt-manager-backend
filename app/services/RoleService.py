"""
Role-related operations service.
Provides the methods to use when interacting with a role.
"""
from fastapi import HTTPException

from app.models.pydantic.PermissionsModel import PydanticPermissionsModel
from app.models.pydantic.RoleModel import PydanticRoleModel
from app.models.tortoise.role import RoleInDB
from app.utils.enums.http_errors import CommonErrorMessages


async def get_all_roles() -> list[PydanticRoleModel]:
    """
        This method retrieves all roles.
    """

    roles: list[RoleInDB] = await RoleInDB.all().prefetch_related("permissions")
    roles_list = []

    for role in roles:

        permissions = [
            PydanticPermissionsModel(**await permission.to_dict())
            for permission in role.permissions
        ]


        role_dict = PydanticRoleModel(
            role_name=role.role_name,
            role_description=role.role_description,
            permissions=permissions
        )

        roles_list.append(role_dict)

    return roles_list

async def get_role_by_id(role_name: str) -> PydanticRoleModel:
    """
        This method retrieves a role.
    """
    role: RoleInDB | None = await RoleInDB.get_or_none(role_name=role_name).prefetch_related("permissions")

    if role is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    print("\nRole details:")
    print(f"Role Name: {role.role_name}")
    print(f"Role Description: {role.role_description}")

    # Affiche les permissions associées
    permissions = ", ".join(str(permission) for permission in role.permissions)
    print(f"Permissions: {permissions}")


    permissions = [
        PydanticPermissionsModel.from_orm(permission)
        for permission in role.permissions
    ]


    role_dict = PydanticRoleModel(
        role_name=role.role_name,
        role_description=role.role_description,
        permissions=permissions
    )

    return role_dict


async def add_role(role: RoleInDB) -> PydanticRoleModel:

    return None


async def modify_role(role_id, body) -> None :

    return None


async def delete_role(role_name) -> None:
    role: RoleInDB | None = await RoleInDB.get_or_none(role_name=role_name)

    if role is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    await role.delete()