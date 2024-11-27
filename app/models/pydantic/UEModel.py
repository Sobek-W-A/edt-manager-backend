"""
This module provides the UEPydanticModel class.
"""
from typing import List

from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.CourseModel import PydanticCourseModel


class PydanticUEModel(AcademicYearPydanticModel):

    ue_id: int
    name: str
    courses: List[PydanticCourseModel]

