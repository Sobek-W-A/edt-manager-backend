"""
This module provides the OperationPydanticModel class.
"""
from pydantic import BaseModel


class PydanticOperationModel(BaseModel):

    operation_id: int
    name: str
    description: str

