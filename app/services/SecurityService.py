"""
This module handles the security operations such as user authentication with login and password 
and hashing of passwords.
"""
from typing import Optional

import bcrypt
from passlib.context import CryptContext

from app.models.tortoise.account import AccountInDB


pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    This Method is designed to get the Hash of a password
    """
    password_hash: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return password_hash.decode('utf-8')

async def authenticate_user(login: str,
                            password: str) -> Optional["AccountInDB"]:
    """
    This method allows us to authenticate the user referenced by the login, 
    using the password provided.
    Args:
        login:    Login for the user.
        password: Password used to check the authenticity of the connection.
    Returns:
        AccountInDB: The account if the user is authenticated, None otherwise.
    """
    # Checking if the user exists or not and checking its password.
    account: AccountInDB | None = await AccountInDB.get_or_none(login=login)
    if account is None or not verify_password(account, password):
        return None
    return account

def verify_password(account: AccountInDB,
                    password: str) -> bool:
    """
    This method will compare a hash provided with the hash of the object concerned.
    """
    return bcrypt.checkpw(password.encode('utf-8'), account.hash.encode('utf-8'))
