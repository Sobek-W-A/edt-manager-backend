"""
Account services. Basically the real functionalities concerning the account model.
"""

import random
import string
from typing import Annotated, Optional, TypeAlias

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from tortoise.expressions import Q

from app.models.pydantic.AccountModel import (PydanticAccountModel,
                                              PydanticAccountPasswordResponse,
                                              PydanticCreateAccountModel,
                                              PydanticModifyAccountModel)
from app.models.pydantic.RoleModel import (PydanticRoleResponseModel,
                                           PydanticSetRoleToAccountModel)
from app.models.pydantic.TokenModel import PydanticToken
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.account_metadata import AccountMetadataInDB
from app.models.tortoise.role import RoleInDB
from app.services import SecurityService
from app.services.PermissionService import check_permissions
from app.services.Tokens import AvailableTokenAttributes, JWTData, Token
from app.utils.CustomExceptions import LoginAlreadyUsedException
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import (AvailableOperations,
                                              AvailableServices)


async def get_account(account_id: int, current_account: AccountInDB) -> PydanticAccountModel:
    """
    This method retrieves an account by its ID.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    account: AccountInDB | None = await AccountInDB.get_or_none(id=account_id)
    if account is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND.value)

    return PydanticAccountModel.model_validate(account)


async def get_all_accounts(current_account: AccountInDB) -> list[PydanticAccountModel]:
    """
    This method retrieves all accounts.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    accounts: list[AccountInDB] = await AccountInDB.all().prefetch_related("profile")
    return [PydanticAccountModel(login=account.login,
                                 id=account.id,
                                 profile=account.profile[0] if account.profile else None) # type: ignore
                                 for account in accounts]

async def search_account_by_keywords(keywords: str, current_account: AccountInDB) -> list[PydanticAccountModel]:
    """
    This method retrieves accounts that matches the login provided.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    query: Q = Q()
    for keyword in keywords.split(" "):
        query &= Q(login__icontains=keyword)

    return list(
        map(
            PydanticAccountModel.model_validate, 
            await AccountInDB.filter(query).all()
        )
    )


async def create_account(account: PydanticCreateAccountModel,
                         current_account: AccountInDB) -> PydanticAccountPasswordResponse:
    """
    This method creates an account.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)

    if await AccountInDB.filter(login=account.login).exists():
        raise LoginAlreadyUsedException

    # If no password mentionned in the body, we generate one
    if account.password is None:
        char_types: dict[str, str] = {
            "L": string.ascii_uppercase,  # Maj
            "l": string.ascii_lowercase,  # Min
            "d": string.digits,  # Number
            "s": "@$!%*?&"  # Symbol
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


async def delete_account(account_id: int, current_account: AccountInDB) -> None:
    """
    This method deletes an account by its ID.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.DELETE,
                            current_account)

    account: AccountInDB | None = await AccountInDB.get_or_none(id=account_id)

    if account is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND.value)

    await account.delete()


async def modify_account(account_id: int, account: PydanticModifyAccountModel, current_account: AccountInDB) -> None:
    """
    This method modifies an account by its ID.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    account_to_modify: AccountInDB | None = await AccountInDB.get_or_none(id=account_id)

    if account_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND.value)

    if await AccountInDB.filter(login=account.login).exists():
        raise LoginAlreadyUsedException

    if account.password is not None:
        account_to_modify.hash = SecurityService.get_password_hash(account.password)

    try:
        account_to_modify.update_from_dict(account.model_dump(exclude={"password", "password_confirm"},  # type: ignore
                                                              exclude_none=True))  # type: ignore

        if account.password is not None:
            account_to_modify.hash = SecurityService.get_password_hash(account.password)
        await account_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


# This is a token that is provided by the OAuth Scheme.
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
OAuthToken: TypeAlias = Annotated[str, Depends(oauth2_scheme)]


async def get_current_account(token: OAuthToken) -> Optional["AccountInDB"]:
    """
    This method returns the user corresponding to the user ID stored inside the token provided.
    :param token: Token used to extract data from.
    """
    # Trying to decode the token given
    token_pydantic: PydanticToken = PydanticToken(value=token)
    token_model: Token = token_pydantic.export_pydantic_to_model(AvailableTokenAttributes.AUTH_TOKEN.value)
    token_payload: JWTData = token_model.extract_payload()

    account_id: int = token_payload.account_id

    # If we get here, that means we managed to decode the token, and we got an user_id.
    # Then, we try to get a user that corresponds to the user_id
    account: AccountInDB | None = await AccountInDB.get_or_none(id=account_id)

    # Otherwise, we successfully identified as the user in the database!
    return account


async def get_role_account_by_id(account_id : int , current_account : AccountInDB, academic_year:int) -> PydanticRoleResponseModel:
    """
    This method returns the list of roles of an user.
    :param account_id: Account ID.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    metadata: AccountMetadataInDB | None = await AccountMetadataInDB.get_or_none(account_id=account_id, academic_year=academic_year).prefetch_related("role")

    if not metadata:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ACCOUNT_NOT_FOUND.value)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=metadata.role.name)

    if not role:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    return PydanticRoleResponseModel(name=role.name,
                                     description=role.description)


async def set_role_account_by_name(account_id: int, current_account : AccountInDB, body : PydanticSetRoleToAccountModel) -> None:
    """
    This method set the role of an account.
    :param account_id: Account ID, role_name : name of the given role.
    """

    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    account: AccountInDB | None = await AccountInDB.get_or_none(id=account_id)

    if not account:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ACCOUNT_NOT_FOUND.value)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=body.name)

    if not role:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    await AccountMetadataInDB.filter(account_id=account_id,
                                     academic_year=body.academic_year).update(role_id=role.name)
