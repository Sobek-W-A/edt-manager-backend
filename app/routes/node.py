"""
This module provides operations related to nodes.
Those are the "folders" before an UE.
"""
from fastapi import APIRouter, Response

from app.models.aliases import AuthenticatedAccount

from app.models.pydantic.NodeModel import PydanticNodeCreateModel, PydanticNodeModel, PydanticNodeModelWithChildIds, PydanticNodeUpdateModel
from app.routes.tags import Tag
from app.services import NodeService

nodeRouter: APIRouter = APIRouter(prefix="/node")
tag: Tag = {
    "name": "Node",
    "description": "Node-related operations."
}

@nodeRouter.get("/root", status_code=200, response_model=PydanticNodeModelWithChildIds)
async def get_root_node(academic_year: int, current_account: AuthenticatedAccount) -> PydanticNodeModelWithChildIds:
    """
    This method returns the root node of the given academic year.
    """
    return await NodeService.get_root_node(academic_year, current_account)

@nodeRouter.get("/{node_id}", status_code=200, response_model=PydanticNodeModelWithChildIds)
async def get_node_by_id(node_id: int, academic_year: int, current_account: AuthenticatedAccount) ->  PydanticNodeModelWithChildIds:
    """
    This method returns the node of the given node id.
    Also returns the contents of the sub-nodes.
    """
    return await NodeService.get_node_by_id(node_id, current_account)

@nodeRouter.get("/root/arborescence", status_code=200, response_model=PydanticNodeModel)
async def get_arborescence_from_root(academic_year: int, current_account: AuthenticatedAccount) -> PydanticNodeModel:
    """
    This method returns the arborescence starting from the root node.
    """
    return await NodeService.get_root_arborescence(academic_year, current_account)

@nodeRouter.get("/{node_id}/arborescence", status_code=200, response_model=PydanticNodeModel)
async def get_arborescence_from_node(academic_year: int, node_id: int, current_account: AuthenticatedAccount) -> PydanticNodeModel:
    """
    This method returns the node of the given academic year and id.
    Also returns the following tree.
    """
    return await NodeService.get_all_child_nodes(node_id, academic_year, current_account)

@nodeRouter.post("/", status_code=201, response_model=PydanticNodeModelWithChildIds)
async def add_node(academic_year: int, node_to_add: PydanticNodeCreateModel, current_account: AuthenticatedAccount) -> PydanticNodeModelWithChildIds:
    """
    This method creates a new node.
    """
    return await NodeService.create_node(academic_year, node_to_add, current_account)

@nodeRouter.patch("/{node_id}", status_code=205)
async def modify_node(academic_year: int, node_id: int, new_data: PydanticNodeUpdateModel, current_account: AuthenticatedAccount) -> Response:
    """
    This method modifies the node of the given node id.
    """
    await NodeService.update_node(academic_year, node_id, new_data, current_account)
    return Response(status_code=205)

@nodeRouter.delete("/{node_id}", status_code=204, response_model=None)
async def delete_node(academic_year: int, node_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This method deletes the node of the given node id.
    """
    await NodeService.delete_node(academic_year, node_id, current_account)
