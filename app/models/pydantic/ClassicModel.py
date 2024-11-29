"""
Pydantic models used for models with name and description.
"""

from pydantic import BaseModel


class ClassicModel(BaseModel):
    """
    Classic model used for the models with name and description
    """
    name: str
    description: str
