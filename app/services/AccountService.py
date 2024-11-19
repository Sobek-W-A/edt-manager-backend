"""
Account services. Basically the real functionalities concerning the account model.
"""


import random
import string

from fastapi import HTTPException

from app.models.pydantic.AccountModel import (PydanticAccountModel, PydanticAccountPasswordResponse,
                                              PydanticCreateAccountModel, PydanticModifyAccountModel)
from app.models.tortoise.account import AccountInDB
from app.services import SecurityService
from app.utils.CustomExceptions import LoginAlreadyUsedException
from app.utils.enums.http_errors import CommonErrorMessages


async def get_account(account_id: int):
    """
    This method retrieves an account by its ID.
    """
    account : AccountInDB | None = await AccountInDB.get_or_none(id=account_id)
    if account is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND.value)

    return PydanticAccountModel.model_validate(account)


async def get_all_accounts():
    """
    This method retrieves all accounts.
    """
    accounts : list[AccountInDB] = await AccountInDB.all()
    return [PydanticAccountModel.model_validate(account) for account in accounts]

async def create_account(account: PydanticCreateAccountModel) -> PydanticAccountPasswordResponse:
    """
    This method creates an account.
    """
    if await AccountInDB.get_or_none(login=account.login):
        raise LoginAlreadyUsedException

    # If no password mentionned in the body, we generate one
    if account.password is None:
        char_types: dict[str, str] = {
            "L": string.ascii_uppercase,  # Maj
            "l": string.ascii_lowercase,  # Min
            "d": string.digits,           # Number
            "s": "@$!%*?&"                # Symbol
        }

        #The schema of our password
        schema: str = "Llllddss"

        password: str = "".join(random.choice(char_types[char]) for char in schema if char in char_types)
    else:
        password: str = account.password

    # We hash the password
    hashed: str = SecurityService.get_password_hash(password)


    account_to_create: AccountInDB = AccountInDB(login=account.login,
                                                 hash=hashed)
    await account_to_create.save()

    return PydanticAccountPasswordResponse(password=password)


async def delete_account(account_id: int) -> None:
    """
    This method deletes an account by its ID.
    """

    account: AccountInDB | None = await AccountInDB.get_or_none(id=account_id)

    if account is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND.value)
    
    await account.delete()

async def modify_account(account_id: int, account: PydanticModifyAccountModel) -> None:
    """
    This method modifies an account by its ID.
    """

    account_to_modify: AccountInDB | None = await AccountInDB.get_or_none(id=account_id)

    if account_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)

    if await AccountInDB.filter(login=account.login).exists():
        raise LoginAlreadyUsedException

    if account.password is not None:
        account_to_modify.hash = SecurityService.get_password_hash(account.password)

    try:
        account_to_modify.update_from_dict(account.model_dump(exclude={"password", "password_confirm"}, # type: ignore
                                                              exclude_none=True))                       # type: ignore

        if account.password is not None:
            account_to_modify.hash = SecurityService.get_password_hash(account.password)
        await account_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e