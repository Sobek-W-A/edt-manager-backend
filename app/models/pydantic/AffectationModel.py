"""
Affectation Pydantic models.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PydanticAffectation(BaseModel):
    """
    Represents a class-teacher affectation.
    """
    profile_id : int
    course_id  : int
    hours      : int
    notes      : str | None
    date       : datetime

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

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
