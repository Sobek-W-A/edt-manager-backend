"""
This module is meant to regroup all methods that are loading standard data into the database.
It should use JSON provided in a specific folder.
"""


import json
from typing import Any, Type
from pydantic import BaseModel
from tortoise.models import Model

from app.models.pydantic.AccountMetadataModel import PydanticAccountMetaModelFromJSON
from app.models.pydantic.AccountModel import PydanticAccountModelFromJSON
from app.models.pydantic.CoefficientModel import PydanticCoefficientModelFromJSON
from app.models.pydantic.CourseModel import PydanticCourseModelFromJSON
from app.models.pydantic.CourseTypeModel import PydanticCourseTypeModelFromJSON
from app.models.pydantic.NodeModel import PydanticNodeModelFromJSON
from app.models.pydantic.OperationModel import PydanticOperationModelFromJSON
from app.models.pydantic.PermissionModel import PydanticPermissionModelFromJSON
from app.models.pydantic.ProfileModel import PydanticProfileModelFromJSON
from app.models.pydantic.PydanticRole import PydanticRoleModelFromJSON
from app.models.pydantic.ServiceModel import PydanticServiceModelFromJSON
from app.models.pydantic.StatusModel import PydanticStatusModelFromJSON
from app.models.pydantic.UEModel import PydanticUEModelFromJSON
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.account_metadata import AccountMetadataInDB
from app.models.tortoise.coefficient import CoefficientInDB
from app.models.tortoise.course import CourseInDB
from app.models.tortoise.course_type import CourseTypeInDB
from app.models.tortoise.node import NodeInDB
from app.models.tortoise.operation import OperationInDB
from app.models.tortoise.permission import PermissionInDB
from app.models.tortoise.profile import ProfileInDB
from app.models.tortoise.role import RoleInDB
from app.models.tortoise.service import ServiceInDB
from app.models.tortoise.status import StatusInDB
from app.models.tortoise.ue import UEInDB
from app.services import SecurityService

JSON_FILE_PATH : str = "./app/static/templates/json/"

async def load_persistent_datasets() -> None:
    """
    This method loads all datasets needed for production purposes.
    """
    await load_json_into_model_via_pydantic(OperationInDB,
                                            PydanticOperationModelFromJSON,
                                            "operation_templates.json")
    await load_json_into_model_via_pydantic(ServiceInDB,
                                            PydanticServiceModelFromJSON,
                                            "service_templates.json")
    await load_json_into_model_via_pydantic(PermissionInDB,
                                            PydanticPermissionModelFromJSON,
                                            "permission_templates.json")
    await load_json_into_model_via_pydantic(RoleInDB,
                                            PydanticRoleModelFromJSON,
                                            "role_templates.json")
    await load_json_into_model_via_pydantic(StatusInDB,
                                            PydanticStatusModelFromJSON,
                                            "status_templates.json")
    await load_json_into_model_via_pydantic(CourseTypeInDB,
                                            PydanticCourseTypeModelFromJSON,
                                            "course_type_templates.json")

async def load_dummy_datasets() -> None:
    """
    This method loads all datasets needed for development purposes.
    """
    await load_persistent_datasets()

    await load_json_into_model_via_pydantic(AccountInDB,
                                            PydanticAccountModelFromJSON,
                                            "account_templates.json")
    await load_json_into_model_via_pydantic(AccountMetadataInDB,
                                            PydanticAccountMetaModelFromJSON,
                                            "account_metadata_templates.json")
    await load_json_into_model_via_pydantic(ProfileInDB,
                                            PydanticProfileModelFromJSON,
                                            "profile_templates.json")
    await load_json_into_model_via_pydantic(CoefficientInDB,
                                            PydanticCoefficientModelFromJSON,
                                            "coefficient_templates.json")
    await load_json_into_model_via_pydantic(CourseInDB,
                                            PydanticCourseModelFromJSON,
                                            "course_templates.json")


    await load_json_into_model_via_pydantic(NodeInDB,
                                            PydanticNodeModelFromJSON,
                                            "node_templates.json")
    await load_json_into_model_via_pydantic(UEInDB,
                                            PydanticUEModelFromJSON,
                                            "ue_templates.json")


async def load_json_into_model_via_pydantic(
    model       : Type[Model],
    schema      : Type[BaseModel],
    file_path   : str
) -> None:
    """
    Loads data from a JSON file into a Tortoise model,
    using a Pydantic model for validation and transformation.

    Args:
        model (Type[Model]): Tortoise model class.
        schema (Type[BaseModel]): Pydantic model class.
        file_path (str): Path to the JSON file.

    Returns:
        None
    """
    if await model.all().count() > 0:
        return

    try:
        # Charger les données JSON
        with open(f"{JSON_FILE_PATH}{file_path}", "r", encoding="utf-8") as file:
            raw_data = json.load(file)
        
        if isinstance(raw_data, dict):  # Si le fichier contient un seul objet
            raw_data: list[dict[str, Any]] = [raw_data]

        # Trying to use pydantic to conform JSON data :
        data: list[BaseModel] = [schema(**item) for item in raw_data]
        
        # Insert data into the database
        for item in data:
            element: dict[str, Any] = item.model_dump(exclude_unset=True)

            # Identify and extract m2m fields based on `_m2m` suffix
            m2m_relations = {
                field_name[:-4]: field_value  # Strip `_m2m` to get the actual field name
                for field_name, field_value in element.items()
                if field_name.endswith("_m2m")
            }

            # Remove m2m fields from the main element
            for m2m_field in m2m_relations.keys():
                element.pop(f"{m2m_field}_m2m")

            if "hash" in element:  # Handle hashed fields if needed
                element["hash"] = SecurityService.get_password_hash(element["hash"])

            # Create the model instance
            instance: Model = await model.create(**element)

            # Assign m2m relations
            for field, ids in m2m_relations.items():
                # I'm sorry for the following pylint comments, there is no other way to do what i need to do without it.
                # It is common practice to use the _meta protected attribute in Tortoise, don't worry.
                meta = model._meta          # pylint: disable=protected-access # type: ignore

                if field in meta.m2m_fields:
                    # Fetch related model instances based on IDs
                    related_model    : Type[Model] = meta.fields_map[field].related_model   # pylint: disable=protected-access # type: ignore
                    related_instances: list[Model] = await related_model.filter(id__in=ids) # pylint: disable=protected-access # type: ignore
                    m2m_manager = getattr(instance, field)
                    await m2m_manager.add(*related_instances)


        print(f"INFO:     {len(data)} instances added init {model.__name__}")

    except Exception as e:
        print(f"ERROR:    Failed loading data for model {model.__name__} : {e}")
