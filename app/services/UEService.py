"""
UE-related operations service.
Provides the methods to use when interacting with an UE.
"""


from app.models.pydantic.UEModel import PydanticUEModel

async def get_ue_by_id(ue_id: int) -> PydanticUEModel:


    #TODO
    return None


async def add_ue() -> PydanticUEModel:
    #TODO
    return None



async def modify_ue(ue_id: int, body):
    #TODO
    return None


async def delete_ue(ue_id: int) -> None:
    #TODO
    return None