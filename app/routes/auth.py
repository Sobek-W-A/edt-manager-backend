from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.Tokens import TokenPair
from app.models.pydantic.TokenModel import PydanticTokenPair
from app.models.tortoise.user import UserInDB
from app.utils.http_errors import CommonErrorMessages

authRouter = APIRouter()


@authRouter.post("/login", response_model=PydanticTokenPair)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Checking credentials
    user = await UserInDB.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=CommonErrorMessages.INCORRECT_LOGIN_PASSWORD.value,
            headers={"WWW-Authenticate": "bearer"}
        )

    # Building and giving token
    tokens = TokenPair()
    tokens.generate_tokens(user.id)
    return tokens.get_tokens_in_response()


@authRouter.post("/logout")
async def logout(tokens: PydanticTokenPair):
    # Invalidating tokens
    await tokens.export_pydantic_to_model().revoke_token()
    # Returning a confirmation message
    return {"message": "ok"}


@authRouter.post("/refresh")
async def refresh_user_tokens(tokens: PydanticTokenPair):
    # Refreshing tokens
    token_model = tokens.export_pydantic_to_model()
    token_model.refresh_tokens()
    return token_model.get_tokens_in_response()
