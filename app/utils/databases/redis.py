import os

import redis
from dotenv import load_dotenv


class Redis:

    redis = None

    @classmethod
    async def load_redis(cls):
        load_dotenv(".env")
        pool = redis.ConnectionPool(host=os.environ.get("REDIS_HOST"),
                                    port=os.environ.get("REDIS_PORT"),
                                    db=os.environ.get("REDIS_DB"),
                                    password=os.environ.get("REDIS_PASSWORD"))

        cls.redis = redis.Redis(connection_pool=pool)

    @classmethod
    def get_redis(cls):
        return cls.redis