"""
Pydantic models for account operations.
"""

from typing import Optional
from app.models.pydantic.validator import Login, Password


class PydanticCreateAccountModel():
    """
    Pydantic model for accounts
    """
    login            : Login
    password         : Password
    password_confirm : Password

class PydanticModifyAccountModel():
    """
    Pydantic model for account modification
    """
    login            : Optional[Login]    = None
    password         : Optional[Password] = None
    password_confirm : Optional[Password] = None
