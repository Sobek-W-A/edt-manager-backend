"""
Account Endpoints.
"""
from fastapi import APIRouter

from app.models.pydantic.AccountModel import PydanticCreateAccountModel, PydanticModifyAccountModel
from app.services import AccountService

from app.models.aliases import AuthenticatedAccount

accountRouter: APIRouter = APIRouter(prefix="/account")

@accountRouter.get("/")
async def get_all_accounts(current_account: AuthenticatedAccount):
    return await AccountService.get_all_accounts(current_account)

@accountRouter.get("/{account_id}")
async def get_account(account_id: int, current_account: AuthenticatedAccount):
    return await AccountService.get_account_by_id(account_id, current_account)

@accountRouter.post("/")
async def create_account(account: PydanticCreateAccountModel, current_account: AuthenticatedAccount):
    return await AccountService.create_account(account, current_account)

@accountRouter.patch("/{account_id}")
async def modify_account(account_id: int, account: PydanticModifyAccountModel, current_account: AuthenticatedAccount):
    return await AccountService.modify_account(account_id, account, current_account)

@accountRouter.delete("/{account_id}")
async def delete_account(account_id: int, current_account: AuthenticatedAccount):
    return await AccountService.delete_account(account_id, current_account)
