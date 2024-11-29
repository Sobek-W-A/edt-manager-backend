"""
Account Endpoints.
"""

from fastapi import APIRouter

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.AccountModel import (PydanticAccountModel,
                                              PydanticAccountPasswordResponse,
                                              PydanticCreateAccountModel,
                                              PydanticModifyAccountModel)

from app.models.pydantic.RoleModel import PydanticRoleResponseModel, PydanticSetRoleToAccountModel
from app.routes.tags import Tag
from app.services import AccountService




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
async def create_account(account: PydanticCreateAccountModel,
                         current_account: AuthenticatedAccount) -> PydanticAccountPasswordResponse:
    """
    This method creates an account.
    """
    return await AccountService.create_account(account, current_account)


@accountRouter.patch("/{account_id}", status_code=205)
async def modify_account(account_id: int, account: PydanticModifyAccountModel,
                         current_account: AuthenticatedAccount) -> None:
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


@accountRouter.get("/{account_id}/role/{academic_year}", status_code=200,response_model=PydanticRoleResponseModel)
async def get_role_account_by_ID(account_id: int, academic_year: int, current_account: AuthenticatedAccount) -> PydanticRoleResponseModel:
    """
    This method get an account's roles with the account ID.
    """

    return await AccountService.getRoleAccountByID(account_id, current_account, academic_year)


@accountRouter.patch("/{account_id}/role/", status_code=205)
async def set_role_account_by_id(account_id: int, current_account: AuthenticatedAccount,
                                 body: PydanticSetRoleToAccountModel) -> None:
    """
    This method set an account's roles with the account ID and a body.
    """

    await AccountService.setRoleAccountByName(account_id, current_account, body)

