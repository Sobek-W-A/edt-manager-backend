"""
This module provides methods to manage nodes.
Nodes are the "folders" before an UE.
"""

from fastapi import HTTPException
from app.models.pydantic.NodeModel import PydanticNodeModel
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.node import NodeInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def get_root(academic_year: int) -> NodeInDB:
    """
    This method retrives the root node from the database.
    CAREFUL ! Does not check for permissions.
    """
    root: NodeInDB | None = await NodeInDB.get_or_none(academic_year=academic_year, parent_id=None)\
                                          .prefetch_related("child_nodes")
    if root is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ROOT_NODE_NOT_FOUND.value)
    return root

async def get_node_map(academic_year: int) -> dict[int, NodeInDB]:
    """
    Returns a dict that associates nodes in the database to their ids.
    It fetches ALL the nodes to do so, use sparignly.
    CAREFUL ! Does not check for permissions !
    """
    all_nodes : list[NodeInDB] = await NodeInDB.filter(academic_year=academic_year)\
                                               .prefetch_related("child_nodes")
    return {node.id: node for node in all_nodes}


async def build_tree_recursive(current_node: NodeInDB, node_map: dict[int, NodeInDB]) -> PydanticNodeModel:
    """
    This method builds the tree described by the nodes inside of a pydantic model.
    This method is recursive.
    CAREFUL ! It does not checks for permissions.
    Args:
        current_node (NodeInDB): Node to start the building from.
        node_map (dict[int, NodeInDB]): A dict used to avoid frequent queries to the database.
    Returns:
        PydanticNodeModel : A tree-like structure, completed with he children relationships.
    """
    children: list[PydanticNodeModel] = []
    if current_node.child_nodes is not None:
        for c in await current_node.child_nodes.all():
            child: NodeInDB | None = node_map.get(c.id)
            if child is not None :
                children.append(await build_tree_recursive(child, node_map))

    return PydanticNodeModel(
        id=current_node.id,
        academic_year=current_node.academic_year,
        name=current_node.name,
        child_nodes=children
    )

async def build_node_with_child_id(node: NodeInDB, children: list[NodeInDB]) -> PydanticNodeModel:
    """
    This method builds a node with its children ids.
    Does not build sub-nodes.
    """
    return PydanticNodeModel(
        id=node.id,
        academic_year=node.academic_year,
        name=node.name,
        child_nodes=[c.id for c in children]
    )


async def get_node_by_id(node_id: int, current_account: AccountInDB) -> PydanticNodeModel:
    """
    This method returns the Node of the given node id.
    Also returns the contents of the sub-nodes.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.GET,
        current_account)

    node: NodeInDB | None = await NodeInDB.get_or_none(id=node_id)\
                                          .prefetch_related("child_nodes")
    if node is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)
    if node.child_nodes is not None:
        return await build_node_with_child_id(node, await node.child_nodes.all())
    return PydanticNodeModel.model_validate(node)

async def get_root_node(academic_year: int, current_account: AccountInDB) -> PydanticNodeModel:
    """
    This method returns the root Node of the given academic year.
    Also returns the sub-nodes ids.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.GET,
        current_account)

    root: NodeInDB = await get_root(academic_year)
    if root.child_nodes is not None:
        return await build_node_with_child_id(root, await root.child_nodes.all())

    return PydanticNodeModel.model_validate(root)

async def get_root_arborescence(academic_year: int, current_account: AccountInDB) -> PydanticNodeModel:
    """
    This method returns the complete arborescence starting from the root.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.GET,
        current_account)

    root: NodeInDB                = await get_root(academic_year)
    node_map: dict[int, NodeInDB] = await get_node_map(academic_year)

    return await build_tree_recursive(root, node_map)


async def get_all_child_nodes(node: int | NodeInDB, academic_year: int, current_account: AccountInDB | None = None) -> PydanticNodeModel:
    """
    This method returns the child Nodes of the given node id.
    To avoid re_checking permissions, we pass the current_account as an optional parameter.
    """
    if current_account is not None:
        await check_permissions(
            AvailableServices.NODE_SERVICE,
            AvailableOperations.GET,
            current_account)

    # If the node to search from has not been provided, we fetch it.
    if isinstance(node, int):
        node_temp: NodeInDB | None = await NodeInDB.get_or_none(id=node)\
                                                   .prefetch_related("child_nodes")
        if node_temp is None:
            raise HTTPException(status_code=404,
                                detail=CommonErrorMessages.NODE_NOT_FOUND.value)
        node = node_temp

    # We fetch all the nodes of the given academic year
    # We use an eager loading method since it requires less requests to the database.
    all_nodes : list[NodeInDB] = await NodeInDB.filter(academic_year=academic_year)\
                                               .prefetch_related("child_nodes")

    node_map: dict[int, NodeInDB] = {node.id: node for node in all_nodes}

    print(node_map)

    return await build_tree_recursive(node, node_map)


async def create_node(node_id: int) -> None:
    """
    This method creates a new Node.
    """

async def add_or_modify_arborescence(academic_year: int) -> None:
    """
    This method adds or modifies the arborescence of the given academic year.
    """

async def update_node(node_id: int) -> None:
    """
    This method updates the Node of the given node id.
    """


async def delete_node(node_id: int) -> None:
    """
    This method deletes the Node of the given node id.
    """
