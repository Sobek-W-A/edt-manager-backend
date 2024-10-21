from datetime import timedelta, datetime
from typing import TypedDict

class JWTData(TypedDict):
    user_id: int
    salt: str
    iat: datetime
    exp: timedelta