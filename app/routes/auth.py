"""
Authentication routes.
Used to manage auth operations.
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.routes.tags import Tag
from app.services import AuthService
from app.models.pydantic.TokenModel import PydanticTokenPair
from app.models.pydantic.ClassicResponses import ClassicOkResponse

authRouter = APIRouter(prefix="/auth")
tag: Tag = {
    "name": "Auth",
    "description": "Authentication-related operations."
}


@authRouter.post("/login", response_model=PydanticTokenPair, status_code=200)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> PydanticTokenPair:
    """
    This method logs in the user.
    Checks if credentials are correct.
    """
    return await AuthService.login(form_data.username, form_data.password)


@authRouter.post("/logout", response_model=ClassicOkResponse, status_code=200)
async def logout(tokens: PydanticTokenPair) -> ClassicOkResponse:
    """
    This method logs out the user.
    """
    return await AuthService.logout(tokens)


@authRouter.post("/refresh", response_model=PydanticTokenPair, status_code=200)
async def refresh_user_tokens(tokens: PydanticTokenPair) -> PydanticTokenPair:
    """
    This method refreshes the user's tokens.
    """
    return await AuthService.refresh_user_tokens(tokens)
