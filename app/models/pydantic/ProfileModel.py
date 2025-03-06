"""
This module provides the Profile's DTO using pydantic.
"""
from typing import Optional

from pydantic import BaseModel

from app.models.pydantic.abstract.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.tools.validator import Mail, Name


class PydanticProfileModify(AcademicYearPydanticModel):
    """
    This model is meant to be used as model-check for Profile-modification
    related requests.
    """
    firstname: Optional[Name] = None
    lastname: Optional[Name] = None
    mail: Optional[Mail] = None
    quota: Optional[int] = None
    account_id: Optional[int] = None
    status_id: Optional[int] = None


class PydanticProfileCreate(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to create a new Profile.
    """
    firstname: Name
    lastname: Name
    mail: Mail
    quota: Optional[int] = None
    account_id: Optional[int] = None
    status_id: int = 3  # TODO : Centralize this.


class PydanticProfileResponse(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to return a Profile to the frontend.
    """
    id: int
    firstname: Name
    lastname: Name
    mail: Mail
    quota: Optional[int] = None
    account_id: Optional[int] = None
    status_id: int

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes: bool = True


class PydanticProfileModelFromJSON(BaseModel):
    """
    Pydantic Model for Profile. This model is used to validate and transform JSON data.
    """
    firstname: str
    lastname: str
    mail: str
    quota: int
    academic_year: int
    account_id: Optional[int] = None
    status_id: int

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes: bool = True

class PydanticNumberOfProfile(BaseModel):
    """
    Pydantic model used to get the number of element in the table.
    """
    number_of_profiles_with_account: int
    number_of_profiles_without_account: int


class PydanticProfileAlert(AcademicYearPydanticModel):
    """
    This model is meant to be used when we need to return a Profile to the frontend.
    """
    id: int
    firstname: Name
    lastname: Name
    mail: Mail
    quota: Optional[int] = None
    hours_affected : int
    account_id: Optional[int] = None
    status_id: int

    class Config:
        """
        Config class used to allow the model to be created from a dictionary.
        """
        from_attributes: bool = True


