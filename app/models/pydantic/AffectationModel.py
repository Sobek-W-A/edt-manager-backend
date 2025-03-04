"""
Affectation Pydantic models.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.pydantic.CourseModel import PydanticCourseModel
from app.models.pydantic.ProfileModel import PydanticProfileResponse
from app.models.pydantic.tools.validator import Hours


class PydanticAffectation(BaseModel):
    """
    Represents a class-teacher affectation.
    """
    id       : int
    profile  : PydanticProfileResponse | int
    course   : PydanticCourseModel     | int
    hours    : Hours
    notes    : Optional[str] = None
    date     : datetime
    group    : int

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
    notes      : Optional[str] = None
    group      : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticAffectationInModify(BaseModel):
    """
    Pydantic model for creating an affectation.
    """
    profile_id : Optional[int]   = None
    course_id  : Optional[int]   = None
    hours      : Optional[Hours] = None
    notes      : Optional[str]   = None
    group      : Optional[int]   = None

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticAffectationExport(BaseModel):
    """
    Pydantic model for exporting an affectation.
    """
    id       : int
    profile  : int
    course   : int
    hours    : int
    notes    : Optional[str] = None
    date     : datetime
    group    : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
