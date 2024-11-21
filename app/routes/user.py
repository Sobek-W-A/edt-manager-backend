"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter, Response

from app.models.pydantic.UserModel import (PydanticUserModify,
                                           PydanticUserCreate,
                                           PydanticUserResponse)
from app.models.aliases import AuthenticatedAccount
from app.services import UserService

userRouter: APIRouter = APIRouter(prefix="/user")

@userRouter.post("", status_code=201)
async def create_user(body: PydanticUserCreate, current_account: AuthenticatedAccount) -> None:
    """
    This method creates a new user
    and return his password.
    """
    await UserService.create_user(body, current_account)



@userRouter.patch("/{user_id}", status_code=205)
async def modify_user(user_id: int, user_model: PydanticUserModify, current_account: AuthenticatedAccount) -> Response:
    """
    This controllers is used when modifying user informations.
    """
    await UserService.modify_user(user_id, user_model, current_account)
    return Response(status_code=205)

@userRouter.get("/", response_model=list[PydanticUserResponse], status_code=200)
async def get_all_users(current_account: AuthenticatedAccount) -> list[PydanticUserResponse]:
    """
    Retrieves a list of all users.
    """
    return await UserService.get_all_users(current_account)


@userRouter.get("/{user_id}", response_model=PydanticUserResponse, status_code=200)
async def get_user_by_id(user_id: int, current_account: AuthenticatedAccount) -> PydanticUserResponse:
    """
    Retrieves a user by their ID.
    """
    return await UserService.get_user_by_id(user_id, current_account)

@userRouter.get("/me", response_model=PydanticUserResponse, status_code=200)
async def get_current_user(current_account: AuthenticatedAccount) -> PydanticUserResponse:
    """
    Retrieves data from the currently connected user.
    """
    # TODO : AAAAAAAAAAAAAAA THIS IS A USER, NOT AN ACCOUNT AAAAAAAAAAAAAA
    return PydanticUserResponse.model_validate(current_account)


@userRouter.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This route is used for deleting a user
    """
    await UserService.delete_user(user_id, current_account)
