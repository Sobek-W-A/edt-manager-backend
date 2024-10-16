import os

from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

class Postgresql:

    @staticmethod
    def get_db_url() -> str:
        """
        This method builds the URL that needs to be used to interact with the database.
        :return: The postgresql database URL.
        """
        load_dotenv(".env")

        port = os.getenv(key="POSTGRES_PORT", default="5432")
        host = os.getenv(key="POSTGRES_HOST", default="localhost")
        password = os.getenv(key="POSTGRES_PASSWORD", default=None)
        user = os.getenv(key="POSTGRES_USER", default=None)
        db = os.getenv(key="POSTGRES_DB", default=None)
        dms = "postgres"

        if db is None or password is None or user is None:
            elements_missing = []
            if db is None :
                elements_missing.append("db ")
            if user is None :
                elements_missing.append("user ")
            if password is None :
                elements_missing.append("password ")
            raise Exception("Some parameters are missing : " + str(elements_missing))

        return f"{dms}://{user}:{password}@{host}:{port}/{db}"


    @staticmethod
    def get_available_models():
        """
        This method returns a list of available models.
        These are located inside the tortoise module.
        """
        model_files = list(
            filter(lambda x : x.endswith(".py") and x != "__init__.py", os.listdir("./app/models/tortoise")))
        return map(lambda x : "app.models.tortoise." + x[:-3], model_files)

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
        await Tortoise.init(
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
