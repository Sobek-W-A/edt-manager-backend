"""
This module is meant to regroup all methods that are loading standard data into the database.
It should use JSON provided in a specific folder.
"""

import json
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.service import ServiceInDB
from app.models.tortoise.user import UserInDB
from app.models.tortoise.role import RoleInDB
from app.services import SecurityService

async def load_dummy_datasets() -> None:
    """
    This method loads all datasets needed for development purposes.
    """
    await load_dummy_operations()
    await load_dummy_services()
    await load_dummy_permissions()
    await load_dummy_roles()

    await load_dummy_accounts()
    await load_dummy_users()


async def load_dummy_users() -> None:
    """
    This method loads dummy users from a json file.
    """
    # We ensure that we don't replace any existing data.
    if await UserInDB.all().count() == 0:
        with open('./app/static/templates/json/user_templates.json', 'r', encoding="utf-8") as file:
            # Load the data from the file
            data = json.load(file)
            for user in data["users"]:
                user = UserInDB(mail=user["mail"],
                                firstname=user["firstname"],
                                lastname=user["lastname"])
                await user.save()

async def load_dummy_accounts() -> None:
    """
    This method loads dummy accounts from a json file.
    """
    # We ensure that we don't replace any existing data.
    if await AccountInDB.all().count() == 0:
        with open('./app/static/templates/json/account_templates.json', 'r', encoding="utf-8") as file:
            # Load the data from the file
            data = json.load(file)
            for account in data["accounts"]:
                account_to_create = AccountInDB(login=account["login"],
                                                hash=SecurityService.get_password_hash(account["password"]))
                await account_to_create.save()

async def load_dummy_roles() -> None:
    """
    This method loads dummy roles from a json file.
    """
    # We ensure that we don't replace any existing data.
    if await RoleInDB.all().count() == 0:
        with open('./app/static/templates/json/role_templates.json', 'r', encoding="utf-8") as file:
            # Load the data from the file
            data = json.load(file)
            for role in data["roles"]:
                permissions = role["permissions"]
                available_perms: list[PermissionInDB] = await PermissionInDB.filter(id__in=permissions)
                role = RoleInDB(role_name=role["name"],
                                role_description=role["description"])
                await role.save()
                for perm in available_perms :
                    await role.permissions.add(perm)
                await role.save()

async def load_dummy_permissions() -> None:
    """
    This method loads dummy permissions from a json file.
    """
    # We ensure that we don't replace any existing data.
    if await PermissionInDB.all().count() == 0:
        with open('./app/static/templates/json/permission_templates.json', 'r', encoding="utf-8") as file:
            # Load the data from the file
            data = json.load(file)
            for permission in data["permissions"]:
                permission = PermissionInDB(service_name_id=permission["service_name"],
                                            operation_name_id=permission["operation_name"])
                await permission.save()

async def load_dummy_operations() -> None:
    """
    This method loads dummy operations from a json file.
    """
    # We ensure that we don't replace any existing data.
    if await OperationInDB.all().count() == 0:
        with open('./app/static/templates/json/operation_templates.json', 'r', encoding="utf-8") as file:
            # Load the data from the file
            data = json.load(file)
            for operation in data["operations"]:
                operation = OperationInDB(operation_name=operation["name"],
                                          operation_description=operation["description"])
                await operation.save()

async def load_dummy_services() -> None:
    """
    This method loads dummy services from a json file.
    """
    # We ensure that we don't replace any existing data.
    if await ServiceInDB.all().count() == 0:
        with open('./app/static/templates/json/service_templates.json', 'r', encoding="utf-8") as file:
            # Load the data from the file
            data = json.load(file)
            for service in data["services"]:
                service = ServiceInDB(service_name=service["name"],
                                      service_description=service["description"])
                await service.save()

async def load_persistent_datasets() -> None:
    """
    This method loads all datasets needed for production purposes.
    """
    await load_dummy_operations()
    await load_dummy_services()
    await load_dummy_permissions()
    await load_dummy_roles()
