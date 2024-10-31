"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter, Response

from app.models.pydantic.UserModel import PydanticUserModify, PydanticUserCreate, PydanticUserPasswordResponse

import app.services.UserService as UserService

userRouter: APIRouter = APIRouter(prefix="/user")


@userRouter.post("", status_code=201)
async def create_user(body: PydanticUserCreate) -> PydanticUserPasswordResponse:
    """
    This method creates a new user.
    """
    return await UserService.create_user(body)


@userRouter.patch("/{user_id}", status_code=205)
async def modify_user(user_id: int, user_model: PydanticUserModify) -> Response:
    """
    This controllers is used when modifying user informations.
    """
    await UserService.modify_user(user_id, user_model)
    return Response(status_code=205)
