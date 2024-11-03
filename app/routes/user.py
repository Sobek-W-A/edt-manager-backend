"""
This module provieds a router for the /user endpoint.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Response

from app.models.pydantic.UserModel import PydanticUserModify, PydanticUserCreate, PydanticUserPasswordResponse, PydanticUserResponse

from app.models.tortoise.user import UserInDB
import app.services.UserService as UserService

userRouter: APIRouter = APIRouter(prefix="/user")


@userRouter.post("", status_code=201)
async def create_user(body: PydanticUserCreate) -> PydanticUserPasswordResponse:
    """
    This method creates a new user
    and return his password.
    """
    return await UserService.create_user(body)


@userRouter.patch("/{user_id}", status_code=205)
async def modify_user(user_id: int, user_model: PydanticUserModify, current_user: Annotated[UserInDB, Depends(UserService.get_current_user)]) -> Response:
    """
    This controllers is used when modifying user informations.
    """
    await UserService.modify_user(user_id, user_model, current_user)
    return Response(status_code=205)

@userRouter.get("/", response_model=list[PydanticUserResponse], status_code=200)
async def get_all_users() -> list[PydanticUserResponse]:
    """
    Retrieves a list of all users.
    """
    return await UserService.get_all_users()


@userRouter.get("/{user_id}", response_model=PydanticUserResponse, status_code=200)
async def get_user_by_id(user_id: int) -> PydanticUserResponse:
    """
    Retrieves a user by their ID.
    """
    return await UserService.get_user_by_id(user_id)

@userRouter.delete("/{user_id}", status_code=205)
async def delete_user(user_id: int) -> None:
    """
    This route is used for deleting a user
    """
    await UserService.delete_user(user_id)
