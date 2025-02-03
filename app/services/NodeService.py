"""
This module provides methods to manage nodes.
Nodes are the "folders" before an UE.
"""

from typing import Optional, Union, cast
from fastapi import HTTPException
from app.models.pydantic.NodeModel import (PydanticNodeCreateModel,
                                           PydanticNodeModel,
                                           PydanticNodeModelWithChildIds,
                                           PydanticNodeUpdateModel,
                                           PydanticUEInNodeModel)
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.node import NodeInDB
from app.models.tortoise.ue import UEInDB
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

async def add_ues_to_node_model(node: PydanticNodeModel | PydanticNodeModelWithChildIds, academic_year: int) -> PydanticNodeModel | PydanticNodeModelWithChildIds:
    """
    This method adds the UEs to the given node model.
    """
    children_ues = await UEInDB.filter(parent_id=node.id,
                                       academic_year=academic_year).all()
    for ue in children_ues:
        if node.child_nodes is None:
            node.child_nodes = []
        node.child_nodes.append(PydanticUEInNodeModel.model_validate(ue))

    return node

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
    children: Union[list[PydanticNodeModel], list[PydanticUEInNodeModel]] = []
    if current_node.child_nodes is not None:
        for c in await current_node.child_nodes.all():
            child: NodeInDB | None = node_map.get(c.id)
            if child is not None :
                children.append(await build_tree_recursive(child, node_map))
    
    pydantic_node: PydanticNodeModel = PydanticNodeModel(
        id=current_node.id,
        academic_year=current_node.academic_year,
        name=current_node.name,
        child_nodes=children
    )

    return cast(PydanticNodeModel, await add_ues_to_node_model(pydantic_node, current_node.academic_year))

async def build_node_with_child_id(node: NodeInDB, children: Optional[list[NodeInDB]] = None) -> PydanticNodeModelWithChildIds:
    """
    This method builds a node with its children ids.
    Does not build sub-nodes apart for UEs.
    """
    if children is None:
        children = []

    res = PydanticNodeModelWithChildIds(
        id=node.id,
        academic_year=node.academic_year,
        name=node.name,
        child_nodes=[c.id for c in children]
    )
    return cast(PydanticNodeModelWithChildIds, await add_ues_to_node_model(res, node.academic_year))

async def get_node_by_id(node_id: int, current_account: AccountInDB) -> PydanticNodeModelWithChildIds:
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
    else:
        return await build_node_with_child_id(node)


async def get_root_node(academic_year: int, current_account: AccountInDB) -> PydanticNodeModelWithChildIds:
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
    else:
        return await build_node_with_child_id(root)


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
    return await build_tree_recursive(node, node_map)


async def create_node(academic_year: int, node_to_add: PydanticNodeCreateModel, current_account: AccountInDB) -> PydanticNodeModelWithChildIds:
    """
    This method creates a new Node.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.CREATE,
        current_account)
    
    if node_to_add.parent_id is not None and not await NodeInDB.exists(id=node_to_add.parent_id, academic_year=academic_year):
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)

    node: NodeInDB = NodeInDB(
        academic_year=academic_year,
        name=node_to_add.name,
        parent_id=node_to_add.parent_id
    )

    await node.save()
    return await build_node_with_child_id(node)

async def update_node(academic_year: int, node_id: int, new_data: PydanticNodeUpdateModel, current_account: AccountInDB) -> None:
    """
    This method updates the Node of the given node id.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.UPDATE,
        current_account)

    node_to_update: NodeInDB | None = await NodeInDB.get_or_none(id=node_id, academic_year=academic_year)
    if node_to_update is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)
    
    if new_data.parent_id is not None and not await NodeInDB.exists(id=new_data.parent_id, academic_year=academic_year):
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)

    node_to_update.update_from_dict(new_data.model_dump(exclude_none=True))# type: ignore

    await node_to_update.save()

async def delete_node(academic_year: int, node_id: int, current_account: AccountInDB) -> None:
    """
    This method deletes the Node of the given node id.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.DELETE,
        current_account)

    node_to_delete: NodeInDB | None = await NodeInDB.get_or_none(id=node_id, academic_year=academic_year)\
                                                    .prefetch_related("child_nodes")
    if node_to_delete is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)
    
    if node_to_delete.child_nodes is not None:
        children :list[NodeInDB] = await node_to_delete.child_nodes.all()
        if len(children) > 0:
            raise HTTPException(status_code=400,
                                detail=CommonErrorMessages.NODE_CANT_DELETE_CHILDREN.value)
        
    children_ues = await UEInDB.filter(parent_id=node_to_delete.id,
                                       academic_year=academic_year).all()
    if len(children_ues) > 0:
        raise HTTPException(status_code=400,
                            detail=CommonErrorMessages.NODE_CANT_DELETE_CHILDREN.value)

    await node_to_delete.delete()
