"""
This module collects all custom exceptions that don't fit in any package very well.
"""

from typing import Dict
from fastapi import HTTPException

from app.utils.enums.http_errors import CommonErrorMessages


# Program Exceptions.
class MissingEnvironnmentException(Exception):
    """
    This Exception is meant to be used when a required environnment variable is not specified.
    """

    missing_variable: str

    def __init__(self, missing_variable: str):
        self.missing_variable = missing_variable

        super().__init__(f"The following environnment variable is missing: {self.missing_variable}")

class RequiredFieldIsNone(Exception):
    """
    This Exception is meant to be used when a required class attribute is None.
    """

    def __init__(self, message: str):
        super().__init__(message)


# HTTP Exceptions.
class IncorrectLoginOrPasswordException(HTTPException):
    """
    This Exception is meant to be used when the login or the password provided are incorrect.
    """
    def __init__(self, headers: Dict[str, str] | None = None) -> None:
        super().__init__(401, CommonErrorMessages.INCORRECT_LOGIN_PASSWORD.value, headers)

class CredentialsException(HTTPException):
    """
    This Exception is meant to be used when the token or credentials provided are incorrect.
    """
    def __init__(self, headers: Dict[str, str] | None = None) -> None:
        super().__init__(401, CommonErrorMessages.INVALID_CREDENTIALS.value, headers)
