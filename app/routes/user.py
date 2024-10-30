"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter
from pydantic import ValidationError

from app.models.pydantic.user import CreateUserInDB

import random
import string

from app.models.tortoise.user import UserInDB
from app.utils.CustomExceptions import LoginAlreadyUsedException, MailAlreadyUsedException, MailIncorrectFormatException
from app.models.pydantic.UserModel import PydanticUserModify

import app.services.UserService as UserService

userRouter: APIRouter = APIRouter(prefix="/user")


@userRouter.post("/create")
async def create_user(body: CreateUserInDB):
    """
    This method create a new user.
    """

    #We check if the login or mail are already used

    if await UserInDB.filter(login=body.login).exists():
        raise LoginAlreadyUsedException

    if await UserInDB.get(mail=body.mail).exists():
        raise MailAlreadyUsedException

    #If no password mentionned in the body, we generate one
    if body.password is None:
        char_types = {
            "L": string.ascii_uppercase,  # Maj
            "l": string.ascii_lowercase,  # Min
            "d": string.digits,  # Number
            "s": string.punctuation  # Symbol
        }

        #The schema of our password
        schema = "Llllddss"

        password = "".join(random.choice(char_types[char]) for char in schema if char in char_types)
    else:
        password = body.password

    #We generate a new id based on the last one
    last_user = await UserInDB.all().order_by('-id').first()
    new_id = last_user.id + 1 if last_user else 1

    #We hash the password
    hashed = UserInDB.get_password_hash(password)

    try:
        user = await UserInDB.create(
            id=new_id,
            login=body.login,
            firstname=body.firstname,
            lastname=body.lastname,
            mail=body.mail,
            hash=hashed
        )
    except ValidationError:
        raise MailIncorrectFormatException

    #We return the password withou hashed because the admin need it to give it to the employee
    return "Password : " + password


@userRouter.patch("/{user_id}", status_code=205)
async def modify_user(user_id: int, user_model: PydanticUserModify) -> None:
    """
    This controllers is used when modifying user informations.
    """
    await UserService.modify_user(user_id, user_model)
