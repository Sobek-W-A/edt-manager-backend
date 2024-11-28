"""
This module is meant to regroup all methods that are loading standard data into the database.
It should use JSON provided in a specific folder.
"""


import json
from typing import Any
from pydantic import BaseModel
from tortoise import Model

from app.models.pydantic.AccountModel import PydanticAccountModelFromJSON
from app.models.pydantic.OperationModel import PydanticOperationModelFromJSON
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.service import ServiceInDB
from app.services import SecurityService

JSON_FILE_PATH : str = "./app/static/templates/json/"

async def load_persistent_datasets() -> None:
    """
    This method loads all datasets needed for production purposes.
    """
    await load_json_into_model_via_pydantic(OperationInDB,
                                            PydanticOperationModelFromJSON,
                                            JSON_FILE_PATH + "operation_templates.json")
    await load_json_into_model_via_pydantic(ServiceInDB,
                                            PydanticServiceModelFromJSON,
                                            JSON_FILE_PATH + "operation_templates.json")


async def load_dummy_datasets() -> None:
    """
    This method loads all datasets needed for development purposes.
    """
    await load_persistent_datasets()

    await load_json_into_model_via_pydantic(AccountInDB,
                                            PydanticAccountModelFromJSON,
                                            JSON_FILE_PATH + "account_templates.json")

async def load_json_into_model_via_pydantic(
    model: Model,
    schema: BaseModel.__class__,
    file_path: str
) -> None:
    """
    Charge des données depuis un fichier JSON dans un modèle Tortoise,
    en utilisant un modèle Pydantic pour validation et transformation.

    Args:
        model (Type[T]): Classe du modèle Tortoise.
        schema (Type[P]): Classe du modèle Pydantic.
        file_path (str): Chemin vers le fichier JSON.

    Returns:
        None
    """
    if await model.all().count() > 0:
        return

    try:
        # Charger les données JSON
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
        
        if isinstance(raw_data, dict):  # Si le fichier contient un seul objet
            raw_data: list[dict[str, Any]] = [raw_data]

        # Trying to use pydantic to conform JSON data :
        data: list[BaseModel] = [schema(**item) for item in raw_data]
        
        # Insertion des données dans la base de données
        for item in data:
            element: dict[str, Any] = item.model_dump(exclude_unset=True)
            print(element)

            if "hash" in element:
                element["hash"] = SecurityService.get_password_hash(element["hash"])

            await model.create(**element)

        print(f"INFO:   {len(data)} instances added init {model.__name__}")

    except Exception as e:
        print(f"ERROR:  Failed loading data for model {model.__name__} : {e}")
