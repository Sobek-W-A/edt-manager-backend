"""
Pydantic models for CourseType.
"""
from pydantic import BaseModel

class PydanticCourseTypeModel(BaseModel):
    """
    This model is meant to be used when we need to return a CourseType to the frontend.
    """
    id: int
    name:str
    description : str

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True

class PydanticCourseTypeModelFromJSON(BaseModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    name         : str
    description  : str

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes : bool = True
