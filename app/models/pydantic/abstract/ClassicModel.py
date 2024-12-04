"""
Pydantic models used for models with name and description.
"""

from pydantic import BaseModel


class ClassicModel(BaseModel):
    """
    Classic model used for the models with name and description.
    Avoids re-defining these attributes.
    """
    name        : str
    description : str
