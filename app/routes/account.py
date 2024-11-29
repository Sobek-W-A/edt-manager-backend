"""
Account Endpoints.
"""
from idlelib.autocomplete import AutoComplete

from fastapi import APIRouter

from app.models.pydantic.AccountModel import (PydanticAccountModel,
                                              PydanticAccountPasswordResponse,
                                              PydanticCreateAccountModel,
                                              PydanticModifyAccountModel)
from app.models.pydantic.ClassicModel import ClassicModel
from app.models.pydantic.RoleModel import PydanticRoleModel
from app.routes.tags import Tag
from app.services import AccountService

from app.models.aliases import AuthenticatedAccount

accountRouter: APIRouter = APIRouter(prefix="/account")
tag: Tag = {
    "name": "Account",
    "description": "Account-related operations."
}

@accountRouter.get("/", status_code=200, response_model=list[PydanticAccountModel])
async def get_all_accounts(current_account: AuthenticatedAccount) -> list[PydanticAccountModel]:
    """
    This method returns all the accounts.
    """
    return await AccountService.get_all_accounts(current_account)

@accountRouter.get("/{account_id}", status_code=200, response_model=PydanticAccountModel)
async def get_account(account_id: int, current_account: AuthenticatedAccount) -> PydanticAccountModel:
    """
    This method returns an account by its ID.
    """
    return await AccountService.get_account(account_id, current_account)

@accountRouter.post("/", status_code=201, response_model=PydanticAccountPasswordResponse)
async def create_account(account: PydanticCreateAccountModel, current_account: AuthenticatedAccount) -> PydanticAccountPasswordResponse:
    """
    This method creates an account.
    """
    return await AccountService.create_account(account, current_account)

@accountRouter.patch("/{account_id}", status_code=205)
async def modify_account(account_id: int, account: PydanticModifyAccountModel, current_account: AuthenticatedAccount) -> None:
    """
    This method modifies an account.
    """
    await AccountService.modify_account(account_id, account, current_account)

@accountRouter.delete("/{account_id}", status_code=204)
async def delete_account(account_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This method deletes an account.
    """
    await AccountService.delete_account(account_id, current_account)

@accountRouter.get("/{account_id}/role/", status_code=200, response_model=list[ClassicModel])
async def get_role_account_by_ID(account_id: int, current_account: AuthenticatedAccount) -> list[ClassicModel]:
    """
        This method get an account's roles with the account ID.
    """

    await AccountService.getRoleAccountByID(account_id, current_account)