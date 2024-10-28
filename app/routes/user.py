"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter

from app.models.tortoise.user import CreateUserInDB, UserInDB

userRouter: APIRouter = APIRouter()

@userRouter.post("/create")
async def create_user(form_data : CreateUserInDB):
    """
    This method create a new user.
    """



    return None
