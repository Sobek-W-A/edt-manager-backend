"""
This module provides services to manage Auth Operations.
"""

from app.models.pydantic.TokenModel import PydanticTokenPair
from app.models.tortoise.account import AccountInDB
from app.services import SecurityService
from app.services.Tokens import AvailableTokenAttributes, TokenPair
from app.utils.CustomExceptions import IncorrectLoginOrPasswordException
from app.models.pydantic.ClassicResponses import ClassicOkResponse


async def login(username: str,
                password: str) -> PydanticTokenPair:
    """
    This method checks if the credentials are correct.
    It returns a pair of tokens to access the application.
    """
    # Checking credentials
    account: AccountInDB | None = await SecurityService.authenticate_user(username, password)

    if not account:
        raise IncorrectLoginOrPasswordException()

    # Building and giving token
    tokens: TokenPair = TokenPair()
    tokens.generate_tokens(account.id)
    access_token  : str = str(tokens.access_token.value)
    refresh_token : str = str(tokens.refresh_token.value)

    return PydanticTokenPair(access_token=access_token,
                             refresh_token=refresh_token)

async def logout(tokens: PydanticTokenPair) -> ClassicOkResponse:
    """
    This method logs out the user by invalidating the tokens provided.
    """
    # Invalidating tokens
    token_model: TokenPair = tokens.export_pydantic_to_model()
    token_model.revoke_tokens()

    # Returning a confirmation message
    return ClassicOkResponse()


async def refresh_user_tokens(tokens: PydanticTokenPair) -> PydanticTokenPair:
    """
    This method refreshes the user's tokens.
    It invalidates the current tokens and gives new ones.
    """
    # Refreshing tokens
    token_model: TokenPair = tokens.export_pydantic_to_model(
        AvailableTokenAttributes.REFRESH_TOKEN.value
    )
    token_model.refresh_tokens()

    access_token  : str = str(token_model.access_token.value)
    refresh_token : str = str(token_model.refresh_token.value)

    return PydanticTokenPair(access_token=access_token,
                             refresh_token=refresh_token)
