"""
This module provides the Redis connection pool to use.
"""
import os
from typing import Optional

import redis
from dotenv import load_dotenv


class Redis:
    """
    Helper class that provides the Redis connection pool.
    """

    redis_instance: Optional["redis.Redis[bytes]"] = None

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
    def get_redis(cls) -> Optional["redis.Redis[bytes]"]:
        """
        This method returns the redis connection pool instance.
        """
        if cls.redis_instance is None:
            cls.load_redis()

        return cls.redis_instance
