"""
This module provides methods to manage nodes.
Nodes are the "folders" before an UE.
"""

from typing import Any, Union, cast
from fastapi import HTTPException
from app.models.pydantic.NodeModel import PydanticNodeModel
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.node import NodeInDB
from app.models.tortoise.ue import UEInDB
from app.services.PermissionService import check_permissions
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import AvailableOperations, AvailableServices


async def get_node_by_id(node_id: int, current_account: AccountInDB) -> PydanticNodeModel:
    """
    This method returns the Node of the given node id.
    Also returns the contents of the sub-nodes.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.GET,
        current_account)
    
    node: NodeInDB | None = await NodeInDB.get_or_none(id=node_id).prefetch_related("child_nodes")
    if node is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)

    return PydanticNodeModel.model_validate(node)

async def get_root_node(academic_year: int, current_account: AccountInDB) -> PydanticNodeModel:
    """
    This method returns the root Node of the given academic year.
    Also returns the sub-nodes ids
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.GET,
        current_account)

    root: NodeInDB | None = await NodeInDB.get_or_none(academic_year=academic_year, is_root=True)\
                                          .prefetch_related("child_nodes")
    if root is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.NODE_NOT_FOUND.value)
    return PydanticNodeModel.model_validate(root)

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

    first_node = PydanticNodeModel.model_validate(node)

    # We fetch all the nodes of the given academic year
    # We use an eager loading method since it requires less requests to the database.
    all_nodes : list[NodeInDB] = await NodeInDB.filter(academic_year=academic_year)\
                                               .prefetch_related("child_nodes")


    # Fonction récursive pour construire le modèle Pydantic
    async def build_tree(node: NodeInDB, all_nodes: list[NodeInDB]) -> PydanticNodeModel:
        children: list[Union[int, PydanticNodeModel]] = []
        if node.child_nodes is not None:
            for child_id in node.child_nodes:
                
                child: NodeInDB = 



        # Retourne le modèle Pydantic pour le nœud actuel
        return PydanticNodeModel(
            id=node.id,
            name=node.name,
            is_root=node.is_root,
            academic_year=node.academic_year,
            children=children if children else None
        )

    # Construire l'arborescence complète à partir de la racine
    return await build_tree(first_node, all_nodes)


async def get_all_nodes(academic_year: int, current_account: AccountInDB) -> PydanticNodeModel:
    """
    This method returns the Nodes of the given academic year.
    """
    await check_permissions(
        AvailableServices.NODE_SERVICE,
        AvailableOperations.GET,
        current_account)

    # We fetch the root Node for the current academic year
    node: NodeInDB | None = await NodeInDB.get_or_none(academic_year=academic_year, is_root=True)
    if node is None:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ROOT_NODE_NOT_FOUND.value)

    return await get_all_child_nodes(node.id, academic_year)

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
