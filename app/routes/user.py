"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter

from app.models.pydantic.UserModel import PydanticUserModify

import app.services.UserService as UserService

userRouter: APIRouter = APIRouter(prefix="/user")

@userRouter.patch("/{user_id}", status_code=205)
async def modify_user(user_id: int, user_model: PydanticUserModify) -> None:
    """
    This controllers is used when modifying user informations.
    """
    await UserService.modify_user(user_id, user_model)

@userRouter.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int) -> None:
    """
    This route is used for deleting a user
    """
    await UserService.delete_user(user_id)