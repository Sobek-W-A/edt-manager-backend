"""
This module provides the CoursePydanticModel class.
"""
from typing import List

from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModel


class PydanticCourseModel(AcademicYearPydanticModel):

    course_id: int
    duration : int
    courses_types : List[PydanticCourseTypeModel]
    
