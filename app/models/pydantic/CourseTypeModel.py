"""
This module provides the CourseTypePydanticModel class.
"""

from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel


class PydanticCourseTypeModel(AcademicYearPydanticModel):
    courseType_id: int
    name: str
    description: str


