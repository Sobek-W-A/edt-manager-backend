"""
This module provides the ServicePydanticModel class.
"""
from pydantic import BaseModel


class PydanticServiceModel(BaseModel):

    service_id: int
    name: str
    description: str

