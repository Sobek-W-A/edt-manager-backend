"""
Statut routes.
Used to manage statut operations.
"""

# TODO


from fastapi import APIRouter

from app.models.pydantic.StatusModel import PydanticStatusResponseModel
from app.models.tortoise.status import StatusInDB
from app.routes.tags import Tag

statutRouter: APIRouter = APIRouter(prefix="/status")
tag: Tag = {
    "name": "Statut",
    "description": "Statut-related operations."
}

@statutRouter.get("/{academic_year}",status_code=200, response_model=list[PydanticStatusResponseModel])
async def get_all_status(academic_year: int) -> list[PydanticStatusResponseModel]:
    """
    This method returns the statut of the given statut id.
    """
    return [PydanticStatusResponseModel.model_validate(statut) for statut in await StatusInDB.filter(academic_year=academic_year).all()]

@statutRouter.get("/{statut_id}",status_code=200, response_model=None)
async def get_statut_by_id(statut_id: int) -> None:
    """
    This method returns the statut of the given statut id.
    """
    return None

@statutRouter.post("/", status_code=201, response_model=None)
async def add_statut() -> None:
    """
    This method creates a new statut.
    """
    return None

@statutRouter.patch("/{statut_id}", status_code=205)
async def modify_statut(statut_id: int, body: None) -> None:
    """
    This method modifies the statut of the given statut id.
    """
    return None


@statutRouter.delete("/{statut_id}", status_code=204)
async def delete_statut(statut_id: int) -> None:
    """
    This method deletes the statut of the given statut id.
    """
    return None