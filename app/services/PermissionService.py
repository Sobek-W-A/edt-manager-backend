"""
This module provides a service to check if a user has the permission to perform 
a certain operation on a certain service.
"""

from fastapi import HTTPException
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.account_metadata import AccountMetadataInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.role import RoleInDB
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def check_permissions(service: AvailableServices,
                            operation: AvailableOperations,
                            current_account: AccountInDB,
                            academic_year: tuple[int, int] = (2024,2025)) -> None:
    """
    This method checks if the provided user has the permission to perform the provided 
    operation on the provided service.
    """
    # We fetch the user's role.
    meta : AccountMetadataInDB | None = await AccountMetadataInDB.get_or_none(account_id=current_account.id,
                                                                      academic_year=academic_year[0]).prefetch_related("role")

    if meta is None:
        raise HTTPException(status_code=403, detail=CommonErrorMessages.FORBIDDEN_ACTION)

    role    : RoleInDB | None = meta.role
    if role is None:
        raise HTTPException(status_code=403, detail=CommonErrorMessages.FORBIDDEN_ACTION)

    # We fetch the permissions of the role.
    # We also filter the permissions to get only the ones that match the service and the operation.
    permissions: list[PermissionInDB] = await role.permissions.filter(service_name_id=service.value.service_name,
                                                                      operation_name_id=operation.value.operation_name)

    # If the list is empty, the user does not have the permission.
    # Otherwise, the user has the permission to do the operation on the service.
    if len(permissions) == 0:
        raise HTTPException(status_code=403, detail=CommonErrorMessages.FORBIDDEN_ACTION)

    async def to_dict(self) -> dict:
        """
        Converts the PermissionInDB instance into a dictionary.
        """
        return {"permission_name": self.permission_name}
