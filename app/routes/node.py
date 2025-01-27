"""
This module provides operations related to nodes.
Those are the "folders" before an UE.
"""
from fastapi import APIRouter
from app.models.pydantic.NodeModel import PydanticNodeFrontModel
from app.routes.tags import Tag

nodeRouter: APIRouter = APIRouter(prefix="/node")
tag: Tag = {
    "name": "Node",
    "description": "Node-related operations."
}


@nodeRouter.get("/{academic_year}", status_code=200, response_model=None)
async def get_nodes_by_academic_year(academic_year: int) -> None:
    """
    This method returns the nodes of the given academic year.
    """
    # TODO
    return None










@nodeRouter.get("/{node_id}", status_code=200, response_model=None)
async def get_node_by_id(node_id: int) -> None:
    """
    This method returns the node of the given node id.
    Also returns the contents of the sub-nodes.
    """
    # TODO
    return None






@nodeRouter.post("/", status_code=201, response_model=None)
async def add_node() -> None:
    """
    This method creates a new node.
    """
    # TODO
    return None






@nodeRouter.post("/{academic_year}", status_code=205)
async def add_or_modify_arborescence(academic_year: int, body: PydanticNodeFrontModel) -> None:
    """
    This method adds or modifies the arborescence of the given academic year.
    """
    # TODO
    return None








@nodeRouter.patch("/{node_id}", status_code=205)
async def modify_node(node_id: int, body: None) -> None:
    """
    This method modifies the node of the given node id.
    """
    # TODO
    return None

@nodeRouter.delete("/{node_id}", status_code=204)
async def delete_node(node_id: int) -> None:
    """
    This method deletes the node of the given node id.
    """
    # TODO
    return None
