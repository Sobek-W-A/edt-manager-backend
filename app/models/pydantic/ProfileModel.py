"""
This module provides the Profile's DTO using pydantic.
"""
from typing import Optional

from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.validator import Mail, Name

class PydanticProfileModify(AcademicYearPydanticModel):
    """
    This model is meant to be used as model-check for Profile-modification
    related requests.
    """
    firstname   : Optional[Name] = None
    lastname    : Optional[Name] = None
    mail        : Optional[Mail] = None
    account_id  : Optional[int]  = None

class PydanticProfileCreate(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to create a new Profile.
    """
    firstname:      Name
    lastname:       Name
    mail:           Mail
    account_id:     Optional[int] = None

class PydanticProfileResponse(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to return a Profile to the frontend.
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
        from_attributes : bool = True