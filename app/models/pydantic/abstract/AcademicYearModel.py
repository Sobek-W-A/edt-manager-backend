"""
This module provides the AcademicYearPydanticModel class.
It is meant to be used with all bodies that needs an academic year.
"""
from pydantic import BaseModel

class AcademicYearPydanticModel(BaseModel):
    """
    This class is meant to be used with all bodies that needs an academic year.
    A.K.A : Almost all of them.
    It inherits from BaseModel, so no need to specify it again inside your child model.
    """
    academic_year: int
