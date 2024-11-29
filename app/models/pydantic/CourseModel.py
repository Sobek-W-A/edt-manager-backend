"""
Pydantic models for Course.
"""

from pydantic import BaseModel


class PydanticCourseModelFromJSON(BaseModel):
    """
    Course model for loading data from a JSON file.
    """
    duration        : int
    academic_year   : int
    course_type_id  : int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True
