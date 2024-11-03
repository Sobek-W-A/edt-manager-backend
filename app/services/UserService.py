"""
User-related operations service.
Provides the methods to use when interacting with a user.
"""
from fastapi import HTTPException
from app.models.pydantic.UserModel import PydanticUserModify, PydanticUserResponse
from app.models.tortoise.user import UserInDB
from app.utils.http_errors import CommonErrorMessages


async def modify_user(user_id: int, model: PydanticUserModify):
    """
    This method modifies the user qualified by the id provided.
    """
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
            user_to_modify.hash = UserInDB.get_password_hash(model.password)
        await user_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

async def get_all_users() -> list[PydanticUserResponse]:
    """
    Retrieves all users.
    """
    users = await UserInDB.all()
    return [PydanticUserResponse.model_validate(user) for user in users]  # Use model_validate for each user

async def get_user_by_id(user_id: int) -> PydanticUserResponse:
    """
    Retrieves a user by their ID.
    """
    user = await UserInDB.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    return PydanticUserResponse.model_validate(user)  # Use model_validate to create the response model


async def get_all_users() -> list[PydanticUserResponse]:
    """
    Retrieves all users.
    """
    users = await UserInDB.all()
    return [PydanticUserResponse.model_validate(user) for user in users]  # Use model_validate for each user

async def get_user_by_id(user_id: int) -> PydanticUserResponse:
    """
    Retrieves a user by their ID.
    """
    user = await UserInDB.get_or_none(id=user_id)
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