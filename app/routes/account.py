"""
Account Endpoints.
"""
from fastapi import APIRouter

from app.services import AccountService


accountRouter: APIRouter = APIRouter(prefix="/account")

@accountRouter.get("/")
async def get_all_accounts():
    return await AccountService.get_all_accounts()

@accountRouter.get("/{account_id}")
async def get_account(account_id: int):
    return await AccountService.get_account_by_id(account_id)

@accountRouter.post("/")
async def create_account(account: PydanticCreateAccountModel):
    return await AccountService.create_account(account)

@accountRouter.patch("/{account_id}")
async def modify_account(account_id: int, account: PydanticUpdateAccountModel):
    return await AccountService.modify_account(account_id, account)

@accountRouter.delete("/{account_id}")
async def delete_account(account_id: int):
    return await AccountService.delete_account(account_id)
