"""
This file provides Enums to use as standards to send error details to the Frontend app.
"""

import enum
from typing import Final

from fastapi import HTTPException


class CommonErrorMessages(enum.Enum):
    """
    Enumeration to provide the commonly used error messages inside the API.
    """
    PASSWORDS_DONT_MATCH     : Final[str] = "The passwords provided don't match."
    PASSWORD_NOT_SECURE      : Final[str] = "The password provided is not secure enough."
    LOGIN_ALREADY_USED       : Final[str] = "This login has already been used."
    MAIL_ALREADY_USED        : Final[str] = "This mail address has already been used."
    USER_NOT_FOUND           : Final[str] = "User was not found."
    USER_NOT_ENABLED         : Final[str] = "This user is not enabled."
    INVALID_CREDENTIALS      : Final[str] = "Invalid credentials."
    INCORRECT_LOGIN_PASSWORD : Final[str] = "Incorrect login or password."
    TOKEN_REVOKED            : Final[str] = "The token has been revoked."
    TOKEN_INVALID            : Final[str] = "The token is invalid."
    TOKEN_EXPIRED            : Final[str] = "The token has expired."


class ClassicExceptions(enum.Enum):
    """
    This enumeration provides several HTTPExceptions to use inside the program.
    """
    credential_exception: Final[HTTPException] = HTTPException(
        status_code=401,
        detail=CommonErrorMessages.INVALID_CREDENTIALS,
        headers={"WWW-Authenticate": "bearer"}
    )
