"""
This file provides Enums to use as standards to send error details to the Frontend app.
"""

import enum

# from fastapi import HTTPException


class CommonErrorMessages(enum.StrEnum):
    """
    Enumeration to provide the commonly used error messages inside the API.
    """
    PASSWORDS_DONT_MATCH     = "The passwords provided don't match."
    PASSWORD_NOT_SECURE      = "The password provided is not secure enough."
    LOGIN_ALREADY_USED       = "This login has already been used."
    MAIL_ALREADY_USED        = "This mail address has already been used."
    USER_NOT_FOUND           = "User was not found."
    USER_NOT_ENABLED         = "This user is not enabled."
    INVALID_CREDENTIALS      = "Invalid credentials."
    INCORRECT_LOGIN_PASSWORD = "Incorrect login or password."
    TOKEN_REVOKED            = "The token has been revoked."
    TOKEN_INVALID            = "The token is invalid."
    TOKEN_EXPIRED            = "The token has expired."


# class ClassicExceptions(enum.Enum):
#     """
#     This enumeration provides several HTTPExceptions to use inside the program.
#     """
#     CREDENTIAL_EXCEPTION = HTTPException(
#         status_code=401,
#         detail=CommonErrorMessages.INVALID_CREDENTIALS,
#         headers={"WWW-Authenticate": "bearer"}
#     )
