"""
This module provides the User's DTO using pydantic.
"""
from typing import Optional, Self
from fastapi import HTTPException
from pydantic import BaseModel, model_validator

from app.utils.enums.http_errors import CommonErrorMessages

from .validator import Mail, Password, Name, Login

class PydanticUserBasePassword(BaseModel):
    """
    Base model for the password with validation
    """
    password: Optional[Password] = None
    password_confirm: Optional[Password] = None

    @model_validator(mode="after")
    def check_password(self) -> Self:
        """
        This validator ensures that the two passwords provided match if they are not None.
        This validator ensures that the two passwords are provided together or none.
        """
        if self.password is None and self.password_confirm is None:
            return self

        if (self.password_confirm is None) != (self.password is None):
            raise HTTPException(status_code=422, detail=CommonErrorMessages.PASSWORD_OR_PASSCONFIRM_NOT_SPECIFIED)

        if self.password is not None and self.password != self.password_confirm:
                raise HTTPException(status_code=422, detail=CommonErrorMessages.PASSWORDS_DONT_MATCH)
        return self

class PydanticUserModify(PydanticUserBasePassword):
    """
    This model is meant to be used as model-check for user-modification
    related requests.
    """
    login:            Optional[Login]    = None
    firstname:        Optional[Name]     = None
    lastname:         Optional[Name]     = None
    mail:             Optional[Mail]     = None

class PydanticUserCreate(PydanticUserBasePassword):
    """
    This model is meant to be used when we need to create a new user.
    """
    login:          Login
    firstname:      Name
    lastname:       Name
    mail:           Mail

class PydanticUserResponse(BaseModel):
    """
    This model is meant to be used when we need to return a user to the frontend.
    """
    id:        int
    login:     Login
    firstname: Name
    lastname:  Name
    mail:      Mail
    class Config:
        from_attributes = True

class PydanticUserPasswordResponse(BaseModel):
    """
    This model is meant to be used when we need to return the password of the user.
    """
    password: Password
