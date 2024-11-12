"""
This module provides utility methods to initialize the necessary databases.
"""
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.utils.databases.datasets import load_dummy_datasets, load_persistent_datasets
from app.utils.databases.postgresql import Postgresql
from app.utils.databases.redis_helper import Redis


async def startup_databases(app: FastAPI) -> None:
    """
    This method initializes the needed databases.
    It also loads the dummy data if the current environnment is the development one.
    """
    if Redis.get_redis() is None:
        Redis.load_redis()
    await Postgresql.init_postgres_db(app)

    # Load dummy dataset if in development environment
    load_dotenv(".env")
    if os.getenv("ENVIRONMENT") == "development":
        await load_dummy_datasets()
    else :
        await load_persistent_datasets()
