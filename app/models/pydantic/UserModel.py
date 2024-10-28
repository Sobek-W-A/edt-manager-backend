from typing import Optional, Self
from pydantic import BaseModel, model_validator

from app.utils.http_errors import CommonErrorMessages

from .validator import Mail, Password, Name, Login

class PydanticUserModify(BaseModel):

    login:            Optional[Login]    = None
    password:         Optional[Password] = None
    password_confirm: Optional[Password] = None
    firstname:        Optional[Name]     = None
    lastname:         Optional[Name]     = None
    mail:             Optional[Mail]     = None

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password is not None:
            assert self.password == self.password_confirm, CommonErrorMessages.PASSWORDS_DONT_MATCH
        return self
    
class PydanticUserResponse(BaseModel):

    id:        int
    login:     Login
    firstname: Name
    lastname:  Name
    mail:      Mail