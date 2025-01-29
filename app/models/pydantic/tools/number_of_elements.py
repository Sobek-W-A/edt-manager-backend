"""
Module that provides the number of elements from a table.
"""
from pydantic import BaseModel


class NumberOfElement(BaseModel):
    """
    Pydantic model used to get the number of element in the table.
    """
    number_of_elements: int
