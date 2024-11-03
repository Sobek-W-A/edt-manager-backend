"""
This module handles the security operations such as user authentication with login and password 
and hashing of passwords.
"""
from typing import Optional

import bcrypt
from passlib.context import CryptContext

from app.models.tortoise.user import UserInDB


pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    This Method is designed to get the Hash of a password
    """
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return password_hash.decode('utf-8')

async def authenticate_user(login: str, password: str) -> Optional["UserInDB"]:
    """
    This method allows us to authenticate the user referenced by the login, 
    using the password provided.
    :param login:    Login for the user.
    :param password: Password used to check the authenticity of the connection.
    :return: None value if the user could not be authenticated, a UserInDB otherwise.
    """
    # Checking if the user exists or not and checking its password.
    user = await UserInDB.get_or_none(login=login)
    if user is None or not verify_password(user, password):
        return None
    return user

def verify_password(user: UserInDB, password: str) -> bool:
    """
    This method will compare a hash provided with the hash of the object concerned.
    """
    return bcrypt.checkpw(password.encode('utf-8'), user.hash.encode('utf-8'))
