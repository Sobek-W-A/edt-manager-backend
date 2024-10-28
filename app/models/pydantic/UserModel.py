"""
This module provides the User's DTO using pydantic.
"""
from typing import Optional, Self
from pydantic import BaseModel, model_validator

from app.utils.http_errors import CommonErrorMessages

from .validator import Mail, Password, Name, Login

class PydanticUserModify(BaseModel):
    """
    This model is meant to be used as model-check for user-modification
    related requests.
    """

    login:            Optional[Login]    = None
    password:         Optional[Password] = None
    password_confirm: Optional[Password] = None
    firstname:        Optional[Name]     = None
    lastname:         Optional[Name]     = None
    mail:             Optional[Mail]     = None

    @model_validator(mode="after")
    def check_password(self) -> Self:
        """
        This validator ensures that the two passwords provided match if they are not None.
        """
        if self.password is not None:
            assert self.password == self.password_confirm, CommonErrorMessages.PASSWORDS_DONT_MATCH
        return self

class PydanticUserResponse(BaseModel):
    """
    This model is meant to be used when we need to return a user to the frontend.
    """
    id:        int
    login:     Login
    firstname: Name
    lastname:  Name
    mail:      Mail
