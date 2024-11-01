"""
This module provieds a router for the /user endpoint.
"""
from typing import Annotated
from fastapi import APIRouter, Depends

from app.models.pydantic.UserModel import PydanticUserModify

from app.models.tortoise.user import UserInDB
import app.services.UserService as UserService

userRouter: APIRouter = APIRouter(prefix="/user")

@userRouter.patch("/{user_id}", status_code=205)
async def modify_user(user_id: int, user_model: PydanticUserModify, current_user: Annotated[UserInDB, Depends(UserService.get_current_user)]) -> None:
    """
    This controllers is used when modifying user informations.
    """
    await UserService.modify_user(user_id, user_model, current_user)
