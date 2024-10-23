"""
This module desribes types that do not fit in any category very well.
"""
from datetime import datetime
from typing import TypedDict

class JWTData(TypedDict):
    """
    Class used to describe the encoded data from the JSON Web Tokens.
    """
    user_id: int
    salt: str
    iat: datetime
    exp: datetime
