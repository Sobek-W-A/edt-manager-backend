"""
Pydantic UE models.
"""

from pydantic import BaseModel


class PydanticUEModelFromJSON(BaseModel):
    """
    Pydantic model for loading data from a JSON file.
    """
    name           : str
    courses_id_m2m : list[int]
    academic_year  : int
    parent_id      : int | None

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes: bool = True
