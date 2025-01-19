"""
This module provides operations related to nodes.
Those are the "folders" before an UE.
"""
from fastapi import APIRouter
from app.routes.tags import Tag

nodeRouter: APIRouter = APIRouter(prefix="/node")
tag: Tag = {
    "name": "Node",
    "description": "Node-related operations."
}

@nodeRouter.get("/{node_id}", status_code=200, response_model=None)
async def get_node_by_id(node_id: int) -> None:
    """
    This method returns the node of the given node id.
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
