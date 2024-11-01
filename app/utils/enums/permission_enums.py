"""
This module provides Enums to help manage permissions.
These are basically static data that needs to be stored in database at creation.
They are used to check if a user has the permission to perform a certain operation on a certain service.
"""
import enum

class AvailableOperations(enum.StrEnum):
    """
    Enumeration to provide the available CRUD operations on the available services.
    """
    CREATE = "Create"
    GET    = "Get"
    UPDATE = "Update"
    DELETE = "Delete"

class AvailableServices(enum.StrEnum):
    """
    Enumeration to provide the available services.
    """
    USER_SERVICE = "User Service"
