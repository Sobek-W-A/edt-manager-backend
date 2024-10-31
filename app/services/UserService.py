"""
User-related operations service.
Provides the methods to use when interacting with a user.
"""
import random
import string

from fastapi import HTTPException
from pydantic import ValidationError

from app.models.pydantic import validator
from app.models.pydantic.UserModel import PydanticUserModify, PydanticUserCreate
from app.models.tortoise.user import UserInDB
from app.utils.CustomExceptions import LoginAlreadyUsedException, MailAlreadyUsedException, MailInvalidException
from app.utils.http_errors import CommonErrorMessages


async def modify_user(user_id: int, model: PydanticUserModify):
    """
    This method modifies the user qualified by the id provided.
    """
    user_to_modify: UserInDB | None = await UserInDB.get_or_none(id=user_id)

    if user_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    if await UserInDB.get(mail=model.mail).exists():
        raise MailAlreadyUsedException

    if await UserInDB.filter(login=model.login).exists():
        raise LoginAlreadyUsedException

    try:
        user_to_modify.update_from_dict(
            model.model_dump(exclude={"password", "password_confirm"}, exclude_none=True))  # type: ignore
        if model.password is not None:
            user_to_modify.hash = UserInDB.get_password_hash(model.password)
        await user_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


async def create_user(model: PydanticUserCreate) -> str:
    """
    This method creates a new user.
    """

    #We check if the login or mail are already used

    if await UserInDB.filter(login=model.login).exists():
        raise LoginAlreadyUsedException

    if await UserInDB.filter(mail=model.mail).exists():
        raise MailAlreadyUsedException

    #If no password mentionned in the body, we generate one
    if model.password is None:
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
        validator.is_password(model.password)
        password = model.password

    #We hash the password
    hashed = UserInDB.get_password_hash(password)

    try:
        await UserInDB.create(
            login=model.login,
            firstname=model.firstname,
            lastname=model.lastname,
            mail=model.mail,
            hash=hashed
        )
    except ValidationError as e:
        raise MailInvalidException from e

    #We return the password without hashed because the admin need it to give it to the employee
    return password
