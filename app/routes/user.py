"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter, HTTPException

from app.models.pydantic.UserModel import PydanticUserModify, PydanticUserResponse

import app.services.UserService as UserService

userRouter: APIRouter = APIRouter(prefix="/user")

@userRouter.patch("/{user_id}", status_code=205)
async def modify_user(user_id: int, user_model: PydanticUserModify) -> None:
    """
    This controllers is used when modifying user informations.
    """
    await UserService.modify_user(user_id, user_model)

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
