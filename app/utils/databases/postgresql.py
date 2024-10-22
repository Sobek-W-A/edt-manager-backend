"""
This module loads the instance of the postgres database inside the Tortoise ORM.
"""
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise # type: ignore

from app.utils.CustomExceptions import MissingEnvironnmentException

class Postgresql:
    """
    This class provides data to initialize the connection with the postgres database 
    that the Tortoise ORM uses.
    """

    @staticmethod
    def get_db_url() -> str:
        """
        This method builds the URL that needs to be used to interact with the database.
        :return: The postgresql database URL.
        """
        load_dotenv(".env")

        port = os.getenv(key="POSTGRES_PORT", default="5432")
        host = os.getenv(key="POSTGRES_HOST", default="localhost")

        user = os.getenv(key="POSTGRES_USER", default=None)
        if user is None :
            raise MissingEnvironnmentException("POSTGRES_USER")

        password = os.getenv(key="POSTGRES_PASSWORD", default=None)
        if password is None :
            raise MissingEnvironnmentException("POSTGRES_PASSWORD")

        db = os.getenv(key="POSTGRES_DB", default=None)
        if db is None :
            raise MissingEnvironnmentException("POSTGRES_DB")

        dms = "postgres"

        return f"{dms}://{user}:{password}@{host}:{port}/{db}"


    @staticmethod
    def get_available_models() -> list[str]:
        """
        This method returns a list of available models.
        These are located inside the tortoise module.
        """
        model_files = list(
            filter(lambda x : x.endswith(".py")
                    and x != "__init__.py", os.listdir("./app/models/tortoise")))
        return ["app.models.tortoise." + x[:-3] for x in model_files]

    @staticmethod
    async def init_postgres_db(app: FastAPI) -> None:
        """
        This method initialises the postgres database connection.
        It also initialises the models if they are not already present.
        """
        # Fetching basic data
        url = Postgresql.get_db_url()
        models = Postgresql.get_available_models()        # Listing models available.

        # Initialize Tortoise ORM
        await Tortoise.init( # type: ignore
            db_url=url,
            modules={'models': models}
        )

        # Generate the schema
        await Tortoise.generate_schemas()

        # Register Tortoise ORM with FastAPI
        register_tortoise(
            app,
            db_url=url,
            modules={"models": models},
            generate_schemas=True,
            add_exception_handlers=True,
        )
