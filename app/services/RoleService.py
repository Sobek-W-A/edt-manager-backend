"""
Role-related operations service.
Provides the methods to use when interacting with a role.
"""
from fastapi import HTTPException

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.RoleModel import (PydanticCreateRoleModel,
                                           PydanticRoleResponseModel,
                                           PydanticUpdateRoleModel)
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.role import RoleInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableServices, AvailableOperations


async def get_all_roles(current_account: AuthenticatedAccount) -> list[PydanticRoleResponseModel]:
    """
    This method retrieves all roles.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    roles: list[RoleInDB] = await RoleInDB.all()
    roles_list : list[PydanticRoleResponseModel] = []

    for role in roles:
        role_dict: PydanticRoleResponseModel = PydanticRoleResponseModel(
            name=role.name,
            description=role.description
        )
        roles_list.append(role_dict)

    return roles_list


async def get_role_by_id(name: str, current_account: AuthenticatedAccount) -> PydanticRoleResponseModel:
    """
        This method retrieves a role with given name.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=name)

    if role is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    return PydanticRoleResponseModel(
        name=role.name,
        description=role.description
    )


async def add_role(role: PydanticCreateRoleModel, current_account: AuthenticatedAccount) -> None:
    """
        This method delete a role with given name.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)

    if await RoleInDB.filter(name=role.name).exists():
        raise HTTPException(status_code=409, detail=CommonErrorMessages.ROLE_ALREADY_EXIST.value)

    role_to_create: RoleInDB = RoleInDB(name=role.name, description=role.description)

    await role_to_create.save()

    if role.permissions:
        for permission in role.permissions:
            perm: PermissionInDB | None = await PermissionInDB.get_or_none(id=permission)
            if not perm:
                raise HTTPException(status_code=404, detail=CommonErrorMessages.PERMISSION_NOT_FOUND.value)
            await role_to_create.permissions.add(perm)


async def modify_role(role_name : str, body: PydanticUpdateRoleModel , current_account: AuthenticatedAccount) -> None:
    """
    This method modifies a role with given name.
    """

    #TODO

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=role_name)

    if role is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    return None


async def delete_role(role_name: str, current_account: AuthenticatedAccount) -> None:
    """
    This method delete a role with given name.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.DELETE,
                            current_account)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=role_name)

    if role is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    await role.delete()
