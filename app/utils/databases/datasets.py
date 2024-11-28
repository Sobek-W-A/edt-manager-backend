"""
This module is meant to regroup all methods that are loading standard data into the database.
It should use JSON provided in a specific folder.
"""


import json
from typing import cast
from tortoise.models import ModelMeta
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.service import ServiceInDB
from app.models.tortoise.profile import ProfileInDB
from app.models.tortoise.role import RoleInDB
from app.services import SecurityService

JSON_FILE_PATH : str = "./app/static/templates/json/"

async def load_dummy_datasets() -> None:
    """
    This method loads all datasets needed for development purposes.
    """
    await load_persistent_datasets()

    await load_json_into_model(AccountInDB, "account_templates.json")


async def load_persistent_datasets() -> None:
    """
    This method loads all datasets needed for production purposes.
    """
    # await load_operations()
    # await load_services()
    # await load_permissions()
    # await load_roles()


# async def load_profiles() -> None:
#     """
#     This method loads dummy profiles from a json file.
#     """
#     # We ensure that we don't replace any existing data.
#     if await ProfileInDB.all().count() == 0:
#         with open('./app/static/templates/json/profile_templates.json', 'r', encoding="utf-8") as file:
#             # Load the data from the file
#             data = json.load(file)
#             for profile in data["profiles"]:
#                 profile = ProfileInDB(mail=profile["mail"],
#                                       firstname=profile["firstname"],
#                                       lastname=profile["lastname"])
#                 await profile.save()

# async def load_accounts() -> None:
#     """
#     This method loads dummy accounts from a json file.
#     """
#     # We ensure that we don't replace any existing data.
#     if await AccountInDB.all().count() == 0:
#         with open('./app/static/templates/json/account_templates.json', 'r', encoding="utf-8") as file:
#             # Load the data from the file
#             data = json.load(file)
#             for account in data["accounts"]:
#                 account_to_create = AccountInDB(login=account["login"],
#                                                 hash=SecurityService.get_password_hash(account["password"]))
#                 await account_to_create.save()

# async def load_roles() -> None:
#     """
#     This method loads roles from a json file.
#     """
#     # We ensure that we don't replace any existing data.
#     if await RoleInDB.all().count() == 0:
#         with open('./app/static/templates/json/role_templates.json', 'r', encoding="utf-8") as file:
#             # Load the data from the file
#             data = json.load(file)
#             for role in data["roles"]:
#                 permissions = role["permissions"]
#                 available_perms: list[PermissionInDB] = await PermissionInDB.filter(id__in=permissions)
#                 role = RoleInDB(name=role["name"],
#                                 description=role["description"])
#                 await role.save()
#                 for perm in available_perms :
#                     await role.permissions.add(perm)
#                 await role.save()

# async def load_permissions() -> None:
#     """
#     This method loads permissions from a json file.
#     """
#     # We ensure that we don't replace any existing data.
#     if await PermissionInDB.all().count() == 0:
#         with open('./app/static/templates/json/permission_templates.json', 'r', encoding="utf-8") as file:
#             # Load the data from the file
#             data = json.load(file)
#             for permission in data["permissions"]:
#                 permission = PermissionInDB(service_name_id=permission["service_name"],
#                                             operation_name_id=permission["operation_name"])
#                 await permission.save()

# async def load_operations() -> None:
#     """
#     This method loads operations from a json file.
#     """
#     # We ensure that we don't replace any existing data.
#     if await OperationInDB.all().count() == 0:
#         with open('./app/static/templates/json/operation_templates.json', 'r', encoding="utf-8") as file:
#             # Load the data from the file
#             data = json.load(file)
#             for operation in data["operations"]:
#                 operation = OperationInDB(name=operation["name"],
#                                           description=operation["description"])
#                 await operation.save()

# async def load_services() -> None:
#     """
#     This method loads services from a json file.
#     """
#     # We ensure that we don't replace any existing data.
#     if await ServiceInDB.all().count() == 0:
#         with open('./app/static/templates/json/service_templates.json', 'r', encoding="utf-8") as file:
#             # Load the data from the file
#             data = json.load(file)
#             for service in data["services"]:
#                 service = ServiceInDB(name=service["name"],
#                                       description=service["description"])
#                 await service.save()


async def load_json_into_model(model: ModelMeta, file_name: str):
    """
    Load data from a JSON file into a Tortoise model, hashing any keys named 'hash'.
    
    Args:
        model (ModelMeta): Tortoise model class.
        file_name (str): Name of the JSON file, with the .json extension.
        
    Returns:
        None
    """
    try:
        # Load JSON data from the file
        with open(f'{JSON_FILE_PATH}{file_name}', "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure data is a list
        if isinstance(data, dict):  # in case we get a single object
            data = [data]

        if not isinstance(data, list):
            raise ValueError("The JSON file must contain an object or a list of objects.")

        # Process each item to hash keys named 'hash'
        for item in data:
            if "hash" in item and isinstance(item["hash"], str):
                item["hash"] = SecurityService.get_password_hash(cast(str, item["hash"]))

        # Bulk create the data in the Tortoise model
        await model.bulk_create([model(**item) for item in data])
        print(f"{len(data)} instances added to {model.__name__}")

    except Exception as e:
        print(f"Error loading data into model {model.__name__}: {e}")
