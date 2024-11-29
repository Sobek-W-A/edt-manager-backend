"""
UE-related operations service.
Provides the methods to use when interacting with an UE.
"""
from app.models.pydantic.UEModel import PydanticCreateUEModel, PydanticUEModel

async def get_ue_by_id(ue_id: int) -> PydanticUEModel:
    """
    This method returns the UE of the given UE id.
    """

    #TODO
    return PydanticUEModel(academic_year=[2024, 2025],
                           courses=[],
                           name="UE",
                           ue_id=1)


async def add_ue(body: PydanticCreateUEModel) -> PydanticUEModel:
    """
    This method creates a new UE.
    """
    #TODO
    return PydanticUEModel(academic_year=[2024, 2025],
                           courses=[],
                           name="UE",
                           ue_id=1)


async def modify_ue(ue_id: int, body: PydanticCreateUEModel) -> None:
    """
    This method modifies the UE of the given UE id.
    """
    #TODO
    return None


async def delete_ue(ue_id: int) -> None:
    """
    This method deletes the UE of the given UE id.
    """
    #TODO
    return None
