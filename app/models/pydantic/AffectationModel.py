"""
Affectation Pydantic models.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.pydantic.tools.validator import Hours


class PydanticAffectation(BaseModel):
    """
    Represents a class-teacher affectation.
    """
    id         : int
    profile_id : int
    course_id  : int
    hours      : Hours
    notes      : str | None
    date       : datetime
    group      : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticAffectationFromJSON(BaseModel):
    """
    Pydantic model for loading data from a JSON file.
    """
    profile_id    : int
    course_id     : int
    hours         : int
    notes         : Optional[str] = None
    date          : datetime
    group         : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticAffectationInCreate(BaseModel):
    """
    Pydantic model for creating an affectation.
    """
    profile_id : int
    course_id  : int
    hours      : Hours
    notes      : str | None
    date       : datetime
    group      : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
