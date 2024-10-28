"""
Authentication routes.
Used to manage auth operations.
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.Tokens import AvailableTokenAttributes, TokenPair
from app.models.pydantic.TokenModel import PydanticTokenPair
from app.models.tortoise.user import UserInDB
from app.utils.CustomExceptions import IncorrectLoginOrPasswordException

authRouter = APIRouter(prefix="/auth")


@authRouter.post("/login", response_model=PydanticTokenPair)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    This method logs in the user.
    Checks if credentials are correct.
    """
    # Checking credentials
    user = await UserInDB.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise IncorrectLoginOrPasswordException()

    # Building and giving token
    tokens = TokenPair()
    tokens.generate_tokens(user.id)
    return tokens.get_tokens_in_response()


@authRouter.post("/logout")
async def logout(tokens: PydanticTokenPair):
    """
    This method logs out the user.
    """
    # Invalidating tokens
    token_model = tokens.export_pydantic_to_model()
    token_model.revoke_tokens()
    # Returning a confirmation message
    return {"message": "ok"}


@authRouter.post("/refresh")
async def refresh_user_tokens(tokens: PydanticTokenPair):
    """
    This method refreshes the user's tokens.
    """
    # Refreshing tokens
    token_model = tokens.export_pydantic_to_model(AvailableTokenAttributes.REFRESH_TOKEN.value)
    token_model.refresh_tokens()
    return token_model.get_tokens_in_response()
