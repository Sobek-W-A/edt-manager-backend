"""
This module is made to provide different user models to the API.
It contains pydantic and Tortoise models.
"""
from typing import Annotated, Optional

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from tortoise import fields
from tortoise.models import Model

from app.models.pydantic.TokenModel import PydanticToken

pwd_context   = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserInDB(Model):
    """
    This class is designed to design the table inside of the database.
    It contains all the columns necessary to store the user.
    """
    id = fields.IntField(primary_key=True)
    login = fields.CharField(unique=True, required=True, max_length=128)
    firstname = fields.CharField(max_length=128)
    lastname = fields.CharField(max_length=128)
    mail = fields.CharField(unique=True, required=True, max_length=128)
    hash = fields.TextField(required=True)

    def __str__(self):
        """
        This method will output a str describing the UserInDB class.
        """
        return "[INFO] - USER " + self.login + " ID : " + str(self.id)

    @staticmethod
    def get_password_hash(password) -> str :
        """
        This Method is designed to get the Hash of a password
        """
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return password_hash.decode('utf-8')


    @staticmethod
    async def authenticate_user(login: str, password: str) -> Optional["UserInDB"] :
        """
        This method allows us to authenticate the user referenced by the login, using the password provided.
        :param login:    Login for the user.
        :param password: Password used to check the authenticity of the connection.
        :return: None value if the user could not be authenticated, a UserInDB otherwise.
        """
        # Checking if the user exists or not and checking its password.
        user = await UserInDB.get_or_none(login=login)
        if user is None or not user.__verify_password(password):
            return None
        return user


    @staticmethod
    async def get_current_user(token: Annotated[PydanticToken, Depends(oauth2_scheme)]) -> Optional["UserInDB"]:
        """
        This method returns the user corresponding to the user ID stored inside the token provided.
        :param token: Token used to ectract data from.
        """

        # Trying to decode the token given
        token_payload = await token.extract_payload()
        user_id: str = token_payload.get("user_id", None)

        # If we manage to decode the token, but user_id is None, we raise a credentials' exception.
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials.",
                headers={"WWW-Authenticate": "bearer"}
            )

        # If we get here, that means we managed to decode the token, and we got an user_id.
        # Then, we try to get a user that corresponds to the user_id
        user = await UserInDB.get_or_none(id=user_id)

        # If the user was not found, we raise another exception.
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials.",
                headers={"WWW-Authenticate": "bearer"}
            )

        # Otherwise, we successfully identified as the user in the database!
        return user

    def __verify_password(self, password) -> bool:
        """
        This method will compare a hash provided with the hash of the object concerned.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.hash.encode('utf-8'))

    class Meta:
        """
        This class is used to indicate the name of the Table to create inside the database.
        """
        table = "User"
