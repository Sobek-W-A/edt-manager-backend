"""
Profile-related operations service.
Provides the methods to use when interacting with a profile.
"""

from fastapi import HTTPException
from pydantic import ValidationError
from tortoise.expressions import Q

from app.models.pydantic.ProfileModel import (PydanticProfileCreate,
                                              PydanticProfileModify,
                                              PydanticProfileResponse)
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.profile import ProfileInDB
from app.services.PermissionService import check_permissions
from app.utils.CustomExceptions import (MailAlreadyUsedException,
                                        MailInvalidException)
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import (AvailableOperations,
                                              AvailableServices)


async def modify_profile(profile_id: int, model: PydanticProfileModify, current_account: AccountInDB) -> None:
    """
    This method modifies the profile qualified by the id provided.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.UPDATE, current_account)

    profile_to_modify: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)

    if profile_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    if await ProfileInDB.filter(mail=model.mail).exists():
        raise MailAlreadyUsedException

    try:
        profile_to_modify.update_from_dict(model.model_dump(exclude_none=True))    # type: ignore
        await profile_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

async def create_profile(model: PydanticProfileCreate, current_account: AccountInDB) -> None:
    """
    This method creates a new profile.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.CREATE, current_account)

    #We check if the login or mail are already used
    if await ProfileInDB.filter(mail=model.mail).exists():
        raise MailAlreadyUsedException

    try:
        await ProfileInDB.create(
            firstname=model.firstname,
            lastname=model.lastname,
            mail=model.mail
        )
    except ValidationError as e:
        raise MailInvalidException from e

async def get_all_profiles(current_account: AccountInDB) -> list[PydanticProfileResponse]:
    """
    Retrieves all profiles.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.GET, current_account)

    profiles: list[ProfileInDB] = await ProfileInDB.all()
    return [PydanticProfileResponse.model_validate(profile) for profile in profiles]  # Use model_validate for each profile

async def get_profile_by_id(profile_id: int, current_account: AccountInDB) -> PydanticProfileResponse:
    """
    Retrieves a profile by their ID.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.GET, current_account)

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    return PydanticProfileResponse.model_validate(profile)  # Use model_validate to create the response model

async def get_current_profile(current_account: AccountInDB) -> PydanticProfileResponse:
    """
    Retrieves the current profile.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.GET, current_account)

    profile : ProfileInDB | None = await ProfileInDB.get_or_none(account=current_account.id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    return PydanticProfileResponse.model_validate(profile)

async def search_profile_by_keywords(keywords: str, current_account: AccountInDB) -> list[PydanticProfileResponse]:
    """
    Searches for a profile by keywords.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    query: Q = Q()
    for keyword in keywords.split(" "):
        query &= (
            Q(lastname__icontains=keyword) |
            Q(firstname__icontains=keyword)
        )

    profiles: list[ProfileInDB] = await ProfileInDB.filter(query).all()
    return [PydanticProfileResponse.model_validate(profile) for profile in profiles]

async def delete_profile(profile_id: int, current_account: AccountInDB) -> None:
    """
    This method deletes the profile by id
    raise exception if profile is not found
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.DELETE, current_account)

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)

    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    await profile.delete()
