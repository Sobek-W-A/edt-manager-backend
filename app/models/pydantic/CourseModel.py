"""
This module provides the CoursePydanticModel class.
"""


from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel


class PydanticCourseModel(AcademicYearPydanticModel):

    course_id: int
    duration : int
    
