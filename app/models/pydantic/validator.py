"""
This module provides different type annotations with pydantic validators.
"""
from fastapi import HTTPException
import regex as re
from typing_extensions import Annotated

from pydantic.functional_validators import AfterValidator

from app.utils.enums.http_errors import CommonErrorMessages

def is_mail(string: str) -> str:
    """
    Checks if a sting is a mail using the regex ``^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$``
    """
    if re.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", string) is None:
        raise HTTPException(status_code=400, detail=CommonErrorMessages.MAIL_INVALID)
    return string

Mail = Annotated[str, AfterValidator(is_mail)]

def is_password(string: str | None) -> str | None:
    """
    Checks if a string is a password (i.e. at least 8 caracters: a lowercase,
    an uppercase, a digit and a special caracter)
    """
    if string is None:
        return string

    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", string) is None:
        raise HTTPException(status_code=400, detail=CommonErrorMessages.PASSWORD_NOT_SECURE)
    return string

Password = Annotated[str, AfterValidator(is_password)]

def is_name(string: str) -> str:
    """
    Checks if a string is a name (i.e. only alphabetical characters and spaces)
    """
    if re.match(r"^[\p{L}\s]+$", string) is None:
        raise HTTPException(status_code=400, detail=CommonErrorMessages.NAME_INVALID)
    return string

Name = Annotated[str, AfterValidator(is_name)]

def is_login(string: str) -> str:
    """
    Checks if a string is a login (i.e. only alphabetical characters, 
    digits and underscores, and at least 5 caracters)
    """
    if re.match(r"^[a-zA-Z0-9_]+$", string) is None:
        raise HTTPException(status_code=400, detail=CommonErrorMessages.LOGIN_INVALID)
    return string

Login = Annotated[str, AfterValidator(is_login)]
