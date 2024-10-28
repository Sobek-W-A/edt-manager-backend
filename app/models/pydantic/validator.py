"""
This module provides different type annotations with pydantic validators.
"""
import regex as re
from typing_extensions import Annotated

from pydantic.functional_validators import AfterValidator

from app.utils.http_errors import CommonErrorMessages

def is_mail(string: str) -> str:
    """
    Checks if a sting is a mail using the regex ``^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$``
    """
    assert re.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", string), CommonErrorMessages.MAIL_INVALID
    return string

Mail = Annotated[str, AfterValidator(is_mail)]

def is_password(string: str) -> str:
    """
    Checks if a string is a password (i.e. at least 8 caracters: a lowercase, an uppercase, a digit and a special caracter)
    """
    assert re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", string), CommonErrorMessages.PASSWORD_NOT_SECURE
    return string

Password = Annotated[str, AfterValidator(is_password)]

def is_name(string: str) -> str:
    """
    Checks if a string is a name (i.e. only alphabetical characters and spaces)
    """
    assert re.match(r"^[\p{L}\s]+$", string), CommonErrorMessages.NAME_INVALID
    return string

Name = Annotated[str, AfterValidator(is_name)]

def is_login(string: str) -> str:
    """
    Checks if a string is a login (i.e. only alphabetical characters, digits and underscores, and at least 5 caracters)
    """
    assert re.match(r"^[a-zA-Z0-9_]+$", string), CommonErrorMessages.LOGIN_INVALID
    return string

Login = Annotated[str, AfterValidator(is_login)]
