
"""
This module provides a service to check if a user has the permission to perform a certain operation on a certain service.
"""

from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.role import RoleInDB
from app.models.tortoise.user import UserInDB
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def check_permissions(current_user: UserInDB, service: AvailableServices, operation: AvailableOperations) -> bool:
    """
    This method checks if the provided user has the permission to perform the provided operation on the provided service.
    """
    
    # We fetch the user's role.
    await current_user.fetch_related("role")
    role: RoleInDB = current_user.role

    # We fetch the permissions of the role.
    permissions: list[PermissionInDB] = await role.fetch_related("permissions") # type: ignore



    return False