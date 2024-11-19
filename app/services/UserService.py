"""
User-related operations service.
Provides the methods to use when interacting with a user.
"""

from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from app.models.pydantic.TokenModel import PydanticToken
from app.models.pydantic.UserModel import (PydanticUserCreate,
                                           PydanticUserModify,
                                           PydanticUserPasswordResponse,
                                           PydanticUserResponse)
from app.models.tortoise.user import UserInDB
from app.services import SecurityService
from app.services.PermissionService import check_permissions
from app.services.Tokens import AvailableTokenAttributes, JWTData, Token
from app.utils.CustomExceptions import (LoginAlreadyUsedException,
                                        MailAlreadyUsedException,
                                        MailInvalidException)
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import (AvailableOperations,
                                              AvailableServices)

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def modify_user(user_id: int, model: PydanticUserModify, current_user: UserInDB) -> None:
    """
    This method modifies the user qualified by the id provided.
    """
    await check_permissions(current_user, AvailableServices.USER_SERVICE, AvailableOperations.UPDATE)

    user_to_modify: UserInDB | None = await UserInDB.get_or_none(id=user_id)

    if user_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    if await UserInDB.filter(mail=model.mail).exists():
        raise MailAlreadyUsedException

    if await UserInDB.filter(login=model.login).exists():
        raise LoginAlreadyUsedException

    try:
        user_to_modify.update_from_dict(model.model_dump(exclude={"password", "password_confirm"}, exclude_none=True)) # type: ignore
        if model.password is not None:
            user_to_modify.hash = SecurityService.get_password_hash(model.password)
        await user_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Optional["UserInDB"]:
    """
    This method returns the user corresponding to the user ID stored inside the token provided.
    :param token: Token used to extract data from.
    """
    # Trying to decode the token given
    token_pydantic: PydanticToken = PydanticToken(value=token)
    token_model:    Token = token_pydantic.export_pydantic_to_model(AvailableTokenAttributes.AUTH_TOKEN.value)
    token_payload:  JWTData = token_model.extract_payload()

    account_id: int = token_payload.account_id

    # If we get here, that means we managed to decode the token, and we got an user_id.
    # Then, we try to get a user that corresponds to the user_id
    user: UserInDB | None = await UserInDB.get_or_none(id=account_id)

    # Otherwise, we successfully identified as the user in the database!
    return user


async def create_user(model: PydanticUserCreate) -> PydanticUserPasswordResponse:
    """
    This method creates a new user.
    """

    #We check if the login or mail are already used
    if await UserInDB.filter(mail=model.mail).exists():
        raise MailAlreadyUsedException

    try:
        await UserInDB.create(
            firstname=model.firstname,
            lastname=model.lastname,
            mail=model.mail
        )
    except ValidationError as e:
        raise MailInvalidException from e

    #We return the password without hashed because the admin need it to give it to the employee
    return PydanticUserPasswordResponse(password=password)

async def get_all_users() -> list[PydanticUserResponse]:
    """
    Retrieves all users.
    """
    users: list[UserInDB] = await UserInDB.all()
    return [PydanticUserResponse.model_validate(user) for user in users]  # Use model_validate for each user

async def get_user_by_id(user_id: int) -> PydanticUserResponse:
    """
    Retrieves a user by their ID.
    """
    user: UserInDB | None = await UserInDB.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    return PydanticUserResponse.model_validate(user)  # Use model_validate to create the response model

async def delete_user(user_id: int):
    """
    This method deletes the user by id
    raise exception if user is not found
    """
    user: UserInDB | None = await UserInDB.get_or_none(id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    await user.delete()
