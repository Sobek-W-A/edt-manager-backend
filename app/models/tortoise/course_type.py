"""
This module contains the CourseTypeInDB model which is used to store
different types of courses.
"""
from app.models.tortoise.abstract.academic_year import AcademicYear
from app.models.tortoise.abstract.classic_model import ClassicModel


class CourseTypeInDB(AcademicYear, ClassicModel):
    """
    This model represents a course type that can be assigned to a course.
    """

    class Meta(AcademicYear.Meta, ClassicModel.Meta):
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        abstract : bool = False
        table    : str  = "CourseType"
