"""
Account Endpoints.
"""
from fastapi import APIRouter


accountRouter: APIRouter = APIRouter(prefix="/account")

@accountRouter.get("/")
async def get_all_accounts():
    pass

@accountRouter.get("/{account_id}")
async def get_account(account_id: int):
    pass

@accountRouter.post("/")
async def create_account():
    pass

@accountRouter.patch("/{account_id}")
async def modify_account(account_id: int):
    pass

@accountRouter.delete("/{account_id}")
async def delete_account(account_id: int):
    pass
