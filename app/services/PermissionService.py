"""
This module provides a service to check if a user has the permission to perform a certain operation on a certain service.
"""

from fastapi import HTTPException
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.role import RoleInDB
from app.models.tortoise.user import UserInDB
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def check_permissions(current_user: UserInDB, service: AvailableServices, operation: AvailableOperations) -> None:
    """
    This method checks if the provided user has the permission to perform the provided operation on the provided service.
    """
    # We fetch the user's role.
    await current_user.fetch_related("role")
    role: RoleInDB = current_user.role

    # We fetch the permissions of the role.
    # We also filter the permissions to get only the ones that match the service and the operation.
    permissions: list[PermissionInDB] = await role.permissions.filter(service_name_id=service.value, operation_name_id=operation.value)

    # If the list is empty, the user does not have the permission.
    # Otherwise, the user has the permission to do the operation on the service.
    if len(permissions) == 0:
        raise HTTPException(status_code=403, detail=CommonErrorMessages.FORBIDDEN_ACTION)
