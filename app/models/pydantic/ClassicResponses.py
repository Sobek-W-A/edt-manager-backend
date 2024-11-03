"""
Simple module that gives Pydantic models for classic responses such as Ok.
"""

from pydantic import BaseModel

class ClassicOkResponse(BaseModel):
    """
    This class is used to describe a classic response with a message.
    """
    message: str = "Ok"
