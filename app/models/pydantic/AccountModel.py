"""
Pydantic models for account operations.
"""

from typing import Optional, Self

from fastapi import HTTPException
from pydantic import BaseModel, model_validator
from app.models.pydantic.ProfileModel import PydanticProfileResponse
from app.models.pydantic.tools.validator import Login, Password
from app.utils.enums.http_errors import CommonErrorMessages


class PydanticAccountBasePassword(BaseModel):
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

class PydanticCreateAccountModel(PydanticAccountBasePassword):
    """
    Pydantic model for accounts.
    """
    login : Login


class PydanticModifyAccountModel(PydanticAccountBasePassword):
    """
    Pydantic model for account modification.
    """
    login : Optional[Login]    = None

class PydanticAccountModel(BaseModel):
    """
    Pydantic model for account retrieval.
    """
    id      : int
    login   : Login
    profile : Optional[PydanticProfileResponse] = None

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
class PydanticAccountWithoutProfileModel(BaseModel):
    """
    Pydantic model for account retrieval.
    """
    id      : int
    login   : Login

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticAccountPasswordResponse(BaseModel):
    """
    This model is meant to be used when we need to return the password of the user.
    """
    password: Password


class PydanticAccountModelFromJSON(BaseModel):
    """
    Pydantic model for account creation, when imported from JSON.
    """
    login : str
    hash  : str

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True


class PydanticNumberOfAccount(BaseModel):
    """
        Pydantic model used to get the number of account in the database.
    """
    number_of_accounts : int
