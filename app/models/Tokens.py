import os
from datetime import datetime, timedelta

import bcrypt
import jwt
import redis
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext

import enum
from typing import Final, TypeAlias

from app.utils.databases.redis import Redis
from app.utils.http_errors import CommonErrorMessages, ClassicExceptions
from utils.CustomExceptions import MissingEnvironnmentException

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenTypes(enum.Enum):
    """
    This enumeration provides the different token types available.
    These types have different secrets and expiration time.
    """
    AUTH_TOKEN:     Final[str] = 'AUTH_TOKEN'
    REFRESH_TOKEN:  Final[str] = 'REFRESH_TOKEN'

class TokenAttributes:

    token_type:  TokenTypes
    expire_time: str
    secret:      str

    def __init__(self, token_type: TokenTypes):
        self.token_type = token_type                                # <- Type of the token. Used to get specific env vars.

        load_dotenv(".env")
        self.algorithm  = os.environ.get("JWT_ALGORITHM", "HS256")  # <- Algorithm used for encoding the tokens

        env_variable_name: str = f"{token_type.value}_EXPIRE"
        self.expire_time = os.environ.get(env_variable_name, None)
        if self.expire_time is None:
            raise MissingEnvironnmentException(env_variable_name)

        env_variable_name: str = f"JWT_{token_type.value}_SECRET_KEY"
        self.secret = os.environ.get(env_variable_name, None)
        if self.secret is None:
            raise MissingEnvironnmentException(env_variable_name)

class AvailableTokenAttributes(enum.Enum):
    """
    This enumeration lists the available token attributes.
    It initializes the values of these attributes with data provided inside the .env file.
    """
    AUTH_TOKEN:    Final[TokenTypes] = TokenAttributes(TokenTypes.AUTH_TOKEN)
    REFRESH_TOKEN: Final[TokenTypes] = TokenAttributes(TokenTypes.REFRESH_TOKEN)


# -------- Classic models -------- #
class Token:
    value: str | None = None
    attributes: TokenAttributes

    def __init__(self, attributes: TokenAttributes, value: str | None = None):
        self.attributes = attributes
        self.value      = value

    def generate(self, user_id: int) -> None:
        """
        This method generates a single token.
        It uses the attributes specified to generate the correct token using the correct private key.
        :return: A Json Web Token.
        """
        # Generating data for the token
        creation_date = datetime.now()
        expire_date = datetime.now() + timedelta(minutes=float(self.attributes.expire_time))
        jwt_data = {
            "user_id": user_id,
            "salt": str(bcrypt.gensalt()),
            "iat": creation_date,
            "exp": expire_date
        }
        self.value = jwt.encode(jwt_data, str(self.attributes.secret), self.attributes.algorithm)

    def revoke(self, redis_db: redis.Redis = Redis.get_redis()) -> None:
        """
        This method handles the necessary operations to revoke the token.
        """
        if self.value is None:
            return

        # Extracting payload
        data = self.extract_payload()
        # Adding the token to redis blocklist with an expiration date according to the expiration date of the token.
        redis_db.setex(self.value, data["exp"], self.attributes.token_type)
        self.value = None

    def extract_payload(self) -> dict | None:
        """
        This method extracts the payload from the current token.
        """

        if self.value is None:
            return None

        # We check if the token has been revoked
        if self.is_revoked():
            raise HTTPException(status_code=401, detail=CommonErrorMessages.TOKEN_REVOKED)

        # We try to extract the payload from the token
        try:
            # We use a different key whether it is a Refresh or an Auth token.
            # Both are supplied in the ENV variables
            data = jwt.decode(jwt=self.value, key=str(self.attributes.secret), algorithms=[self.attributes.algorithm])

        except jwt.exceptions.ExpiredSignatureError:
            # This exception is raised if the date of the token has expired
            raise HTTPException(status_code=401, detail=CommonErrorMessages.TOKEN_EXPIRED)

        except jwt.exceptions.InvalidTokenError:
            # This exception is raised if the token cannot be decoded.
            raise HTTPException(status_code=401, detail=CommonErrorMessages.TOKEN_INVALID)

        # We return the payload
        return data

    def is_revoked(self, redis_db: redis.Redis = Redis.get_redis()) -> bool:
        """
        This method checks if the token has been blacklisted inside Redis DB.
        """
        # We check if the token is revoked (in the redis DB)
        # If the result is None, the token was not revoked
        return not (self.value is None or redis_db.get(self.value) is None)


class TokenPair:
    access_token:  Token
    refresh_token: Token

    def __init__(self, access_token: str | None = None, refresh_token: str | None = None):
        self.access_token  = Token(AvailableTokenAttributes.AUTH_TOKEN.value, access_token)
        self.refresh_token = Token(AvailableTokenAttributes.REFRESH_TOKEN.value, refresh_token)

    def get_tokens_in_response(self) -> dict[str, str]:
        """
        This method provides the object that needs to be returned when we want to send a new token pair.
        """
        return {
            "access_token":  self.access_token.value,
            "refresh_token": self.refresh_token.value,
            "token_type":    "bearer"
        }


    def generate_tokens(self, user_id: int) -> None:
        """
        This method generates a pair of tokens.
        It stores them inside the current object instance.
        """
        self.access_token.generate(user_id)
        self.refresh_token.generate(user_id)


    def revoke_tokens(self) -> None:
        """
        This method revokes the access token and refresh token inside the current object.
        """
        self.access_token.revoke()
        self.refresh_token.revoke()

    def refresh_tokens(self) -> None:
        """
        This method uses the refresh token to create a new access token and refresh token.
        It stores the tokens inside the current object instance.
        """
        if self.refresh_token is None:
            raise Exception("No refresh token was provided ! Aborting refresh...")

        # Trying to decode the token given
        token_payload = self.refresh_token.extract_payload()
        user_id: int = token_payload.get("user_id")

        # If we manage to decode the token, but user_id is None, we raise a credentials' exception.
        if user_id is None:
            raise ClassicExceptions.credential_exception
        # We need to add the refresh_token and the acces_token to the blocklist since it does not (and may not) have expired yet.
        self.revoke_tokens()

        # If we managed to get here, user and token are valid inputs. we can generate both tokens.
        # Generating new tokens
        self.generate_tokens(user_id=user_id)

AvailableTokenModels: TypeAlias = Token | TokenPair
