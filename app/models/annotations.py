
from typing import Annotated, TypeAlias

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.tortoise.account import AccountInDB
from app.services import AccountService

# This is the account that is used in logged requests.
# We can find it using the encrypted tokens provided inside the request's headers.
AuthenticatedAccount : TypeAlias = Annotated[AccountInDB, Depends(AccountService.get_current_account)]

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
# This is a token that is provided by the OAuth Scheme.
OAuthToken : TypeAlias = Annotated[str, Depends(oauth2_scheme)]
