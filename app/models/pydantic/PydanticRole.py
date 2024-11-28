"""
Pydantic Models for Roles.
"""

from pydantic import BaseModel


class PydanticRoleModelFromJSON(BaseModel):
    """
    Pydantic Model for Role. This model is used to validate and transform JSON data.
    """
    name: str
    description: str
    permissions_m2m: list[int]

    class Config:
        """
        Pydantic configuration for Role.
        """
        from_attributes = True
