"""
This module provides the User's DTO using pydantic.
"""
from typing import Optional
from pydantic import BaseModel

from app.models.pydantic.validator import Mail, Name

class PydanticUserModify(BaseModel):
    """
    This model is meant to be used as model-check for user-modification
    related requests.
    """
    firstname   : Optional[Name] = None
    lastname    : Optional[Name] = None
    mail        : Optional[Mail] = None
    account_id  : Optional[int]  = None

class PydanticUserCreate(BaseModel):
    """
    This model is meant to be used when we need to create a new user.
    """
    firstname:      Name
    lastname:       Name
    mail:           Mail
    account_id:     Optional[int] = None

class PydanticUserResponse(BaseModel):
    """
    This model is meant to be used when we need to return a user to the frontend.
    """
    id:         int
    firstname:  Name
    lastname:   Name
    mail:       Mail
    account_id: Optional[int] = None

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes = True
