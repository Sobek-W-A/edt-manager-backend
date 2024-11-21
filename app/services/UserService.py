"""
User-related operations service.
Provides the methods to use when interacting with a user.
"""

from fastapi import HTTPException
from pydantic import ValidationError

from app.models.pydantic.UserModel import (PydanticUserCreate,
                                           PydanticUserModify,
                                           PydanticUserResponse)
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.user import UserInDB
from app.services.PermissionService import check_permissions
from app.utils.CustomExceptions import (MailAlreadyUsedException,
                                        MailInvalidException)
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import (AvailableOperations,
                                              AvailableServices)


async def modify_user(user_id: int, model: PydanticUserModify, current_account: AccountInDB) -> None:
    """
    This method modifies the user qualified by the id provided.
    """
    await check_permissions(AvailableServices.USER_SERVICE, AvailableOperations.UPDATE, current_account)

    user_to_modify: UserInDB | None = await UserInDB.get_or_none(id=user_id)

    if user_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    if await UserInDB.filter(mail=model.mail).exists():
        raise MailAlreadyUsedException

    try:
        user_to_modify.update_from_dict(model.model_dump(exclude_none=True))    # type: ignore
        await user_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

async def create_user(model: PydanticUserCreate, current_account: AccountInDB) -> None:
    """
    This method creates a new user.
    """
    await check_permissions(AvailableServices.USER_SERVICE, AvailableOperations.CREATE, current_account)

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

async def get_all_users(current_account: AccountInDB) -> list[PydanticUserResponse]:
    """
    Retrieves all users.
    """
    await check_permissions(AvailableServices.USER_SERVICE, AvailableOperations.GET, current_account)

    users: list[UserInDB] = await UserInDB.all()
    return [PydanticUserResponse.model_validate(user) for user in users]  # Use model_validate for each user

async def get_user_by_id(user_id: int, current_account: AccountInDB) -> PydanticUserResponse:
    """
    Retrieves a user by their ID.
    """
    await check_permissions(AvailableServices.USER_SERVICE, AvailableOperations.GET, current_account)

    user: UserInDB | None = await UserInDB.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    return PydanticUserResponse.model_validate(user)  # Use model_validate to create the response model

async def get_current_user(current_account: AccountInDB) -> PydanticUserResponse:
    """
    Retrieves the current user.
    """
    await check_permissions(AvailableServices.USER_SERVICE, AvailableOperations.GET, current_account)

    user : UserInDB | None = await UserInDB.get_or_none(account=current_account.id)
    if user is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    return PydanticUserResponse.model_validate(user)

async def delete_user(user_id: int, current_account: AccountInDB) -> None:
    """
    This method deletes the user by id
    raise exception if user is not found
    """
    await check_permissions(AvailableServices.USER_SERVICE, AvailableOperations.DELETE, current_account)

    user: UserInDB | None = await UserInDB.get_or_none(id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    await user.delete()
