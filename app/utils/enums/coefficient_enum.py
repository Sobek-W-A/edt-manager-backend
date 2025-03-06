"""
This module provides Enums to help manage permissions.
These are basically static data that needs to be stored in database at creation.
They are used to check the coefficient of a status
on a certain service.
"""
from app.utils.enums.enum_loaders import LoadableData


class Coefficient(LoadableData):
    multiplier: float
    operation_description: str
