"""
This module is meant to regroup all methods that are loading standard data into the database.
It should use JSON provided in a specific folder.
"""

import json
from app.models.tortoise.user import UserInDB

async def load_dummy_datasets() -> None:
    """
    This method loads all datasets needed for development purposes.
    """
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
                user = UserInDB(login=user["login"],
                                hash=UserInDB.get_password_hash(user["password"]),
                                mail=user["mail"],
                                firstname=user["firstname"],
                                lastname=user["lastname"])
                await user.save()
