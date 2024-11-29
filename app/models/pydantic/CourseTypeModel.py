from pydantic import BaseModel

from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel


class PydanticCourseTypeModel(AcademicYearPydanticModel):

    name:str
    description : str

class PydanticCourseTypeModelFromJSON(BaseModel):
    """
    This class is used to load a JSON file into a Pydantic model.
    """
    name         : str
    description  : str
    academic_year: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes = True
