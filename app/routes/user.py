"""
This module provieds a router for the /user endpoint.
"""
from fastapi import APIRouter

from app.models.tortoise.user import CreateUserInDB, UserInDB

userRouter: APIRouter = APIRouter()

@userRouter.post("/create")
async def create_user(body : CreateUserInDB):
    """
    This method create a new user.
    """

    if body.hash is None:
        print('ici on va generer un mdp aleatoire')

    print("modifier la création de l'id")
    user = await UserInDB.create(
        id=1,
        login=body.login,
        firstname=body.firstname,
        lastname=body.lastname,
        mail=body.mail,
        hash=body.hash
    )


    return user
