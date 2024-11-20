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

def is_academic_year(years: tuple[int, int]) -> tuple[int, int]:
    """
    We check that the tuple contains 2 values and that the second element is 
    equal to the first one + 1.
    """
    if len(years) != 2:
        raise ValueError("Le tuple doit contenir exactement deux éléments.")
    if years[1] != years[0] + 1:
        raise ValueError("Le second élément doit être égal au premier + 1.")
    return years

AcademicYear = Annotated[str, AfterValidator(is_academic_year)]
