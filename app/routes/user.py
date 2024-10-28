"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter
from fastapi.responses import Response

from app.models.pydantic.UserModel import PydanticUserModify, PydanticUserResponse

import app.services.UserService as UserService

userRouter: APIRouter = APIRouter(prefix="/user")

@userRouter.patch("/{user_id}", response_model=PydanticUserResponse)
async def modify_user(user_id: int, user_model: PydanticUserModify) -> Response:
    resp: PydanticUserResponse = await UserService.modify_user(user_id, user_model)
    return Response(content=resp, status_code=205)
