from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class CreateUserInDB(BaseModel):

    login: str = Field(..., min_length=1)
    firstname: str = Field(..., min_length=1)
    lastname: str = Field(..., min_length=1)
    mail: EmailStr = Field(..., min_length=1)
    password: Optional[str] = None