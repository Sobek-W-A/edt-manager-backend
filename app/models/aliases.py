"""
This module provides type aliases and annotations for the FastAPI models.
"""
from typing import Annotated, TypeAlias

from fastapi import Depends

from app.models.tortoise.account import AccountInDB
from app.services import AccountService

# This is the account that is used in logged requests.
# We can find it using the encrypted tokens provided inside the request's headers.
AuthenticatedAccount : TypeAlias = Annotated[AccountInDB, Depends(AccountService.get_current_account)]
