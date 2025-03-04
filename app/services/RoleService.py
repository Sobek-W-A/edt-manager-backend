"""
Role-related operations service.
Provides the methods to use when interacting with a role.
"""
from fastapi import HTTPException

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.PermissionModel import PydanticPermissionModel
from app.models.pydantic.RoleModel import (PydanticCreateRoleModel,
                                              PydanticUpdateRoleModel,
                                              PydanticRoleResponseModel)
from app.models.pydantic.ServiceModel import PydanticServiceModel
from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.role import RoleInDB
from app.models.tortoise.service import ServiceInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableRoles, AvailableServices, AvailableOperations


async def get_all_roles(academic_year: int,
                        current_account: AuthenticatedAccount) -> list[PydanticRoleResponseModel]:
    """
    This method retrieves all roles.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET_MULTIPLE,
                            current_account,
                            academic_year)

    roles:       list[RoleInDB] = await RoleInDB.all()\
                                                .prefetch_related("permissions")
    roles_list : list[PydanticRoleResponseModel] = []

    for role in roles:
        permissions: list[PermissionInDB] = await role.permissions.all()\
                                                                  .prefetch_related("service",
                                                                                    "operation")
        permission_dict: dict[str, list[OperationInDB]] = {}
        services: list[ServiceInDB] = []
        for permission in permissions:
            services.append(permission.service)
            if permission.service.name not in permission_dict:
                permission_dict[permission.service.name] = []
            permission_dict[permission.service.name].append(permission.operation)

        role_dict: PydanticRoleResponseModel = PydanticRoleResponseModel(
                                                name=role.name,
                                                description=role.description,
                                                permissions=[PydanticPermissionModel(
                                                    service=PydanticServiceModel(
                                                        name=service.name,
                                                        description=service.description
                                                    ),
                                                    operations=[operation.name 
                                                                for operation in permission_dict[service.name]
                                                                ]
                                                ) for service in services])
        roles_list.append(role_dict)

    return roles_list


async def get_role_by_id(academic_year: int,
                         name: str,
                         current_account: AuthenticatedAccount) -> PydanticRoleResponseModel:
    """
    This method retrieves a role with given name.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET_SINGLE,
                            current_account,
                            academic_year)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=name)

    if role is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    permissions: list[PermissionInDB] = await role.permissions.all()\
                                                                  .prefetch_related("service",
                                                                                    "operation")
    permission_dict: dict[str, list[OperationInDB]] = {}
    services: list[ServiceInDB] = []
    for permission in permissions:
        services.append(permission.service)
        if permission.service.name not in permission_dict:
            permission_dict[permission.service.name] = []
        permission_dict[permission.service.name].append(permission.operation)

    return PydanticRoleResponseModel(
            name=role.name,
            description=role.description,
            permissions=[PydanticPermissionModel(
                service=PydanticServiceModel(
                    name=service.name,
                    description=service.description
                ),
                operations=[operation.name for operation in permission_dict[service.name]]
            ) for service in services])


async def add_role(academic_year: int,
                   role: PydanticCreateRoleModel,
                   current_account: AuthenticatedAccount) -> None:
    """
    This method delete a role with given name.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.CREATE,
                            current_account,
                            academic_year)

    if await RoleInDB.filter(name=role.name).exists():
        raise HTTPException(status_code=409, detail=CommonErrorMessages.ROLE_ALREADY_EXIST.value)

    role_to_create: RoleInDB = RoleInDB(name=role.name, description=role.description)

    await role_to_create.save()

    if role.permissions:
        for permission in role.permissions:
            perm: PermissionInDB | None = await PermissionInDB.get_or_none(id=permission)
            if not perm:
                raise HTTPException(status_code=404,
                                    detail=CommonErrorMessages.PERMISSION_NOT_FOUND.value)
            await role_to_create.permissions.add(perm)


async def modify_role(academic_year: int,
                      role_name : str,
                      body: PydanticUpdateRoleModel,
                      current_account: AuthenticatedAccount) -> None:
    """
    This method modifies a role with given name.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account,
                            academic_year)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=role_name)

    if role is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    if role.name == AvailableRoles.ADMIN.value.role_name:
        raise HTTPException(status_code=403,
                            detail=CommonErrorMessages.CANNOT_UPDATE_ADMIN.value)

    return None


async def delete_role(academic_year: int,
                      role_name: str,
                      current_account: AuthenticatedAccount) -> None:
    """
    This method delete a role with given name.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.DELETE,
                            current_account,
                            academic_year)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=role_name)

    if role is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    if role.name == AvailableRoles.ADMIN.value.role_name:
        raise HTTPException(status_code=403,
                            detail=CommonErrorMessages.CANNOT_DELETE_ADMIN.value)

    await role.delete()
