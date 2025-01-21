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
                                              PydanticAccountPasswordResponse, PydanticAccountWithoutProfileModel,
                                              PydanticCreateAccountModel,
                                              PydanticModifyAccountModel)
from app.models.pydantic.ProfileModel import PydanticProfileResponse
from app.models.pydantic.PydanticRole import (PydanticRoleResponseModel,
                                             PydanticSetRoleToAccountModel)
from app.models.pydantic.TokenModel import PydanticToken
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.account_metadata import AccountMetadataInDB
from app.models.tortoise.profile import ProfileInDB
from app.models.tortoise.role import RoleInDB
from app.services import SecurityService
from app.services.PermissionService import check_permissions
from app.services.Tokens import AvailableTokenAttributes, JWTData, Token
from app.utils.CustomExceptions import LoginAlreadyUsedException
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import (AvailableOperations,
                                              AvailableServices)


async def get_account(account_id: int, current_account: AccountInDB) -> PydanticAccountWithoutProfileModel:
    """
    This method retrieves an account by its ID.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    account: AccountInDB | None = await AccountInDB.get_or_none(id=account_id).prefetch_related("profile")
    if account is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND.value)

    return PydanticAccountWithoutProfileModel.model_validate(account)

async def get_accounts_not_linked_to_profile(academic_year: int, current_account: AccountInDB) -> list[PydanticAccountWithoutProfileModel]:
    """
    This method retrieves all accounts not linked to a profile.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)
    accounts: list[AccountInDB] = await AccountInDB.all().prefetch_related("profile")
    accounts_to_return: list[AccountInDB] = []

    for account in accounts:
        if account.profile is not None:
            for profile in await account.profile.all():
                if profile.academic_year != academic_year and account not in accounts_to_return:
                    accounts_to_return.append(account)

    return [PydanticAccountWithoutProfileModel.model_validate(account) for account in accounts]

async def get_all_accounts(current_account: AccountInDB) -> list[PydanticAccountWithoutProfileModel]:
    """
    This method retrieves all accounts.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    accounts: list[AccountInDB] = await AccountInDB.all()
    return [PydanticAccountWithoutProfileModel.model_validate(account) for account in accounts]

async def search_accounts_by_login(keywords: str, current_account: AccountInDB) -> list[PydanticAccountModel]:
    """
    This method fetches the accounts which logins matches the query provided.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)
    
    academic_year: int = 2024   # TODO : Get the current academic year from the url.

    account_query: Q = Q()
    for keyword in keywords.split(" "):
        account_query &= Q(login__icontains=keyword)

    # Fetch accounts and prefetch profiles
    accounts: list[AccountInDB] = await AccountInDB.filter(account_query)\
                                                   .prefetch_related("profile")\
                                                   .all()

    accounts_to_return: list[PydanticAccountModel] = []

    # Process accounts
    for account in accounts:
        prof = None
        if account.profile:
            # We ensure that the profile is from the academic year 2024.
            # We also retrieve the first one manually since Tortoise is weird.
            profile_instance = await account.profile.filter(academic_year=academic_year).first()
            if profile_instance is not None:
                prof = PydanticProfileResponse.model_validate(profile_instance)

        accounts_to_return.append(PydanticAccountModel(id=account.id,
                                                       login=account.login,
                                                       profile=prof))

    return accounts_to_return

async def search_account_by_keywords(keywords: str, current_account: AccountInDB) -> list[PydanticAccountModel]:
    """
    This method retrieves accounts that match the keywords provided.
    The search applies to the following fields: login, firstname, lastname, and email.
    """
    await check_permissions(AvailableServices.ACCOUNT_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    academic_year: int = 2024   # TODO : Get the current academic year from the url.

    account_query: Q = Q()
    profile_query: Q = Q()
    for keyword in keywords.split(" "):
        account_query &= Q(login__icontains=keyword)
        profile_query &= Q(firstname__icontains=keyword) | Q(lastname__icontains=keyword) | Q(mail__icontains=keyword)

    # Fetch accounts and prefetch profiles
    accounts: list[AccountInDB] = await AccountInDB.filter(account_query)\
                                                   .prefetch_related("profile")\
                                                   .all()
    # Fetch profiles directly
    profiles: list[ProfileInDB] = await ProfileInDB.filter(profile_query)\
                                                   .filter(academic_year=academic_year)\
                                                   .prefetch_related("account")\
                                                   .all()

    accounts_to_return: list[PydanticAccountModel] = []
    account_ids: list[int] = []

    # Process accounts
    for account in accounts:
        prof = None
        if account.profile:
            # We ensure that the profile is from the academic year 2024.
            # We also retrieve the first one manually since Tortoise is weird. 
            profile_instance = await account.profile.filter(academic_year=academic_year).first()
            if profile_instance is not None:
                prof = PydanticProfileResponse.model_validate(profile_instance)

        accounts_to_return.append(PydanticAccountModel(id=account.id,
                                                       login=account.login,
                                                       profile=prof))
        account_ids.append(account.id)

    # Process profiles
    for profile in profiles:
        # We make sure we do not select the same account twice.
        if profile.account and profile.account.id not in account_ids:
            accounts_to_return.append(PydanticAccountModel(
                login=profile.account.login,
                id=profile.account.id,
                profile=PydanticProfileResponse.model_validate(profile)
            ))
            account_ids.append(profile.account.id)

    return accounts_to_return

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

    if account.id == current_account.id:
        raise HTTPException(status_code=403,
                            detail=CommonErrorMessages.CANNOT_SET_YOUR_OWN_ROLE)

    role: RoleInDB | None = await RoleInDB.get_or_none(name=body.name)

    if not role:
        raise HTTPException(status_code=404,
                            detail=CommonErrorMessages.ROLE_NOT_FOUND.value)

    await AccountMetadataInDB.filter(account_id=account_id,
                                     academic_year=body.academic_year).update(role_id=role.name)
