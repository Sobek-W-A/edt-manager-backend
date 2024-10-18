"""
This module provides the Redis connection pool to use.
"""
import os

import redis
from dotenv import load_dotenv

from app.utils.CustomExceptions import RequiredFieldIsNone


class Redis:
    """
    Helper class that provides the Redis connection pool.
    """

    redis_instance: redis.Redis | None = None

    @classmethod
    def load_redis(cls) -> None:
        """
        This method loads the redis client by providing the correct credentials.
        """
        load_dotenv(".env")
        pool = redis.ConnectionPool(host=os.environ.get("REDIS_HOST"),
                                             port=os.environ.get("REDIS_PORT"),
                                             db=os.environ.get("REDIS_DB"),
                                             password=os.environ.get("REDIS_PASSWORD"))

        cls.redis_instance = redis.Redis(connection_pool=pool)

    @classmethod
    def get_redis(cls) -> redis.Redis:
        """
        This method returns the redis connection pool instance.
        """
        if cls.redis_instance is None:
            raise RequiredFieldIsNone("Redis client was not properly initialized ! Aborting...")

        return cls.redis_instance
