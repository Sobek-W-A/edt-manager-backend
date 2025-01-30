"""
This module provides operations related to nodes.
Those are the "folders" before an UE.
"""
from fastapi import APIRouter

from app.models.aliases import AuthenticatedAccount

from app.models.pydantic.NodeModel import PydanticNodeFrontModel, PydanticNodeModel
from app.routes.tags import Tag
from app.services import NodeService

nodeRouter: APIRouter = APIRouter(prefix="/node")
tag: Tag = {
    "name": "Node",
    "description": "Node-related operations."
}

@nodeRouter.get("/id/{node_id}", status_code=200, response_model=PydanticNodeModel)
async def get_node_by_id(node_id: int, current_account: AuthenticatedAccount) ->  PydanticNodeModel:
    """
    This method returns the node of the given node id.
    Also returns the contents of the sub-nodes.
    """
    return await NodeService.get_node_by_id(node_id, current_account)

@nodeRouter.get("/root/{academic_year}", status_code=200, response_model=PydanticNodeModel)
async def get_root_node(academic_year: int, current_account: AuthenticatedAccount) -> PydanticNodeModel:
    """
    This method returns the root node of the given academic year.
    """
    return await NodeService.get_root_node(academic_year, current_account)

@nodeRouter.get("/root/arborescence/{academic_year}", status_code=200, response_model=PydanticNodeModel)
async def get_arborescence_from_root(academic_year: int, current_account: AuthenticatedAccount) -> PydanticNodeModel:
    """
    This method returns the arborescence starting from the root node.
    """
    return await NodeService.get_root_arborescence(academic_year, current_account)

@nodeRouter.get("/{node_id}/arborescence/{academic_year}", status_code=200, response_model=PydanticNodeModel)
async def get_arborescence_from_node(academic_year: int, node_id: int,current_account: AuthenticatedAccount) -> PydanticNodeModel:
    """
    This method returns the node of the given academic year and id.
    Also returns the following tree.
    """
    return await NodeService.get_all_child_nodes(node_id, academic_year, current_account)


@nodeRouter.post("/", status_code=201, response_model=None)
async def add_node(current_account: AuthenticatedAccount) -> None:
    """
    This method creates a new node.
    """
    # TODO
    return None

@nodeRouter.post("/{academic_year}", status_code=205)
async def add_or_modify_arborescence(academic_year: int, body: PydanticNodeFrontModel, current_account: AuthenticatedAccount) -> None:
    """
    This method adds or modifies the arborescence of the given academic year.
    """
    # TODO
    return None

@nodeRouter.patch("/{node_id}", status_code=205)
async def modify_node(node_id: int, body: None, current_account: AuthenticatedAccount) -> None:
    """
    This method modifies the node of the given node id.
    """
    # TODO
    return None

@nodeRouter.delete("/{node_id}", status_code=204)
async def delete_node(node_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This method deletes the node of the given node id.
    """
    # TODO
    return None
