"""
This module is used to provide utility classes to manage Tokens.
It provides models and methods to do so.
"""

import enum
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, TypeAlias

import bcrypt
from jwt import encode, decode, exceptions  # type: ignore
import redis
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext
from app.utils.CustomExceptions import MissingEnvironnmentException, RequiredFieldIsNone

from app.utils.databases.redis_helper import Redis
from app.utils.enums.http_errors import CommonErrorMessages

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTData():
    """
    Class used to describe the encoded data from the JSON Web Tokens.
    """
    account_id: int
    salt: str
    iat: datetime
    exp: datetime

    def __init__(self, account_id: int, salt: str, iat: datetime, exp: datetime):
        self.account_id = account_id
        self.salt = salt
        self.iat = iat
        self.exp = exp

    def export(self) -> dict[str, Any]:
        """
        Exports the JWTData to a dictionary.
        """
        return {
            "account_id": self.account_id,
            "salt": self.salt,
            "iat": self.iat,
            "exp": self.exp
        }

class TokenTypes(enum.Enum):
    """
    This enumeration provides the different token types available.
    These types have different secrets and expiration time.
    """
    AUTH_TOKEN    = 'AUTH_TOKEN'
    REFRESH_TOKEN = 'REFRESH_TOKEN'

class TokenAttributes:
    """
    This class provides environnment information about a Token in a cleaner way.
    """

    token_type:  TokenTypes
    expire_time: str
    secret:      str

    def __init__(self, token_type: TokenTypes):
        # Type of the token. Used to get specific env vars.
        self.token_type = token_type

        load_dotenv(".env")

        # Algorithm used for encoding the tokens
        self.algorithm: str  = os.environ.get("JWT_ALGORITHM", "HS256")

        env_variable_name: str = f"{token_type.value}_EXPIRE"
        temp: str | None = os.environ.get(env_variable_name, None)
        if temp is None:
            raise MissingEnvironnmentException(env_variable_name)
        self.expire_time = temp

        env_variable_name: str = f"JWT_{token_type.value}_SECRET_KEY"
        temp: str | None = os.environ.get(env_variable_name, None)
        if temp is None:
            raise MissingEnvironnmentException(env_variable_name)
        self.secret = temp

class AvailableTokenAttributes(enum.Enum):
    """
    This enumeration lists the available token attributes.
    It initializes the values of these attributes with data provided inside the .env file.
    """
    AUTH_TOKEN    = TokenAttributes(TokenTypes.AUTH_TOKEN)
    REFRESH_TOKEN = TokenAttributes(TokenTypes.REFRESH_TOKEN)


# -------- Classic models -------- #
class Token:
    """
    This class represents a single Token.
    It uses the Attributes specified by a specific instance of TokenAttributes.
    """

    value      : str | None      = None
    attributes : TokenAttributes

    def __init__(self, attributes: TokenAttributes, value: str | None = None):
        self.attributes = attributes
        self.value      = value

    def generate(self, account_id: int) -> None:
        """
        This method generates a single token.
        It uses the attributes specified to generate the correct token using the 
        correct private key.
        :return: A Json Web Token.
        """
        # Generating data for the token
        creation_date: datetime = datetime.now(tz=timezone.utc)
        expire_date: datetime   = datetime.now() + timedelta(minutes=float(self.attributes.expire_time))

        jwt_data: JWTData = JWTData(account_id=account_id,
                                    salt=str(bcrypt.gensalt()),
                                    iat=creation_date,
                                    exp=expire_date)

        self.value = encode(payload=jwt_data.export(),
                                key=self.attributes.secret,
                                algorithm=self.attributes.algorithm)

    def revoke(self, redis_db: Optional["redis.Redis[bytes]"] = Redis.get_redis()) -> None:
        """
        This method handles the necessary operations to revoke the token.
        """
        if self.value is None:
            return

        if redis_db is None:
            raise RequiredFieldIsNone("Redis instance is None !")

        # Extracting payload
        data: JWTData = self.extract_payload()
        # Adding the token to redis blocklist with an expiration equal to
        # the expiration date - creation date.
        ttl: timedelta = data.exp - data.iat
        redis_db.setex(self.value, ttl, self.attributes.token_type.value)
        self.value = None

    def extract_payload(self) -> JWTData:
        """
        This method extracts the payload from the current token.
        """

        # We check if the token has been revoked
        if self.is_revoked():
            raise HTTPException(status_code=401, detail=CommonErrorMessages.TOKEN_REVOKED)

        # We try to extract the payload from the token
        try:
            # We use a different key whether it is a Refresh or an Auth token.
            # Both are supplied in the ENV variables
            if self.value is not None:
                data: Any = decode(jwt=self.value,
                                       key=str(self.attributes.secret),
                                       algorithms=[self.attributes.algorithm])

                data = JWTData(account_id=data["account_id"],
                               salt=data["salt"],
                               iat=datetime.fromtimestamp(data["iat"]),
                               exp=datetime.fromtimestamp(data["exp"]))
            else:
                raise RequiredFieldIsNone("Token value is None !")

        except exceptions.ExpiredSignatureError as e:
            # This exception is raised if the date of the token has expired
            raise HTTPException(status_code=401, detail=CommonErrorMessages.TOKEN_EXPIRED) from e

        except exceptions.InvalidTokenError as e:
            # This exception is raised if the token cannot be decoded.
            raise HTTPException(status_code=401, detail=CommonErrorMessages.TOKEN_INVALID) from e

        # We return the payload
        return data

    def is_revoked(self, redis_db: Optional["redis.Redis[bytes]"] = Redis.get_redis()) -> bool:
        """
        This method checks if the token has been blacklisted inside Redis DB.
        """
        # We check if the token is revoked (in the redis DB)
        # If the result is None, the token was not revoked
        if redis_db is None:
            raise RequiredFieldIsNone("Redis instance is None !")
        return not (self.value is None or redis_db.get(self.value) is None)


class TokenPair:
    """
    This class represents a pair of Tokens.
    It uses the Attributes specified by specific instances of TokenAttributes.
    Contains an Access Token and a Refresh Token.
    """

    access_token:  Token
    refresh_token: Token

    def __init__(self, access_token: str | None = None, refresh_token: str | None = None):
        self.access_token  = Token(AvailableTokenAttributes.AUTH_TOKEN.value, access_token)
        self.refresh_token = Token(AvailableTokenAttributes.REFRESH_TOKEN.value, refresh_token)

    def get_tokens_in_response(self) -> dict[str, str | None]:
        """
        This method provides the object that needs to be returned when we want to send 
        a new token pair.
        """
        return {
            "access_token":  self.access_token.value,
            "refresh_token": self.refresh_token.value,
            "token_type":    "bearer"
        }

    def generate_tokens(self, account_id: int) -> None:
        """
        This method generates a pair of tokens.
        It stores them inside the current object instance.
        """
        self.access_token.generate(account_id)
        self.refresh_token.generate(account_id)

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
        # Trying to decode the token given
        token_payload: JWTData = self.refresh_token.extract_payload()
        account_id: int = token_payload.account_id

        # We need to add the refresh_token and the acces_token to the blocklist since it does not
        # (and may not) have expired yet.
        self.revoke_tokens()

        # If we managed to get here, account and token are valid inputs. we can generate both tokens.
        # Generating new tokens
        self.generate_tokens(account_id=account_id)

# This allows us to regroup the Token models into one type.
AvailableTokenModels: TypeAlias = Token | TokenPair
