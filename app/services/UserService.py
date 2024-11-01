"""
User-related operations service.
Provides the methods to use when interacting with a user.
"""
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.models.pydantic.TokenModel import PydanticToken
from app.models.pydantic.UserModel import PydanticUserModify
from app.models.tortoise.user import UserInDB
from app.services import SecurityService
from app.services.PermissionService import check_permissions
from app.services.Tokens import AvailableTokenAttributes, Token
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import (AvailableOperations,
                                              AvailableServices)
from app.utils.type_hint import JWTData

oauth2_scheme:  OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def modify_user(user_id: int, model: PydanticUserModify, current_user: UserInDB) -> None:
    """
    This method modifies the user qualified by the id provided.
    """
    await check_permissions(current_user, AvailableServices.USER_SERVICE, AvailableOperations.UPDATE)

    user_to_modify: UserInDB | None = await UserInDB.get_or_none(id=user_id)

    if user_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    if model.mail and await UserInDB.all().filter(mail=model.mail).count() != 0:
        raise HTTPException(status_code=409, detail=CommonErrorMessages.MAIL_ALREADY_USED)
    
    if model.login and await UserInDB.all().filter(login=model.login).count() != 0:
        raise HTTPException(status_code=409, detail=CommonErrorMessages.LOGIN_ALREADY_USED)

    try:
        user_to_modify.update_from_dict(model.model_dump(exclude={"password", "password_confirm"}, exclude_none=True)) # type: ignore
        if model.password is not None:
            user_to_modify.hash = SecurityService.get_password_hash(model.password)
        await user_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


async def get_current_user(token: Annotated[PydanticToken, Depends(oauth2_scheme)]) -> Optional["UserInDB"]:
    """
    This method returns the user corresponding to the user ID stored inside the token provided.
    :param token: Token used to extract data from.
    """
    # Trying to decode the token given
    token_model:  Token = token.export_pydantic_to_model(AvailableTokenAttributes
                                                         .AUTH_TOKEN.value)
    token_payload: JWTData = token_model.extract_payload()

    user_id: int = token_payload.get("user_id", None)

    # If we get here, that means we managed to decode the token, and we got an user_id.
    # Then, we try to get a user that corresponds to the user_id
    user = await UserInDB.get_or_none(id=user_id)

    # Otherwise, we successfully identified as the user in the database!
    return user
