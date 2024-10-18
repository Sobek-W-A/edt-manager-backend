import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.utils.databases.datasets import load_dummy_datasets
from app.utils.databases.postgresql import Postgresql
from app.utils.databases.redis import Redis


async def startup_databases(app: FastAPI) -> None:
    await Postgresql.init_postgres_db(app)
    Redis.load_redis()

    # Load dummy dataset if in development environment
    if os.getenv("ENVIRONMENT") == "development":
        load_dotenv(".env")
        await load_dummy_datasets()
