"""
Profile-related operations service.
Provides the methods to use when interacting with a profile.
"""

from typing import Any
from fastapi import HTTPException
from pydantic import ValidationError
from tortoise.expressions import Q
from tortoise.queryset import QuerySet

from app.models.pydantic.ProfileModel import (PydanticProfileCreate,
                                              PydanticProfileModify,
                                              PydanticProfileResponse, PydanticNumberOfProfile)

from app.models.pydantic.tools.pagination import PydanticPagination
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.affectation import AffectationInDB
from app.models.tortoise.profile import ProfileInDB
from app.models.tortoise.status import StatusInDB
from app.services.PermissionService import check_permissions
from app.utils.CustomExceptions import (MailAlreadyUsedException, MailInvalidException)
from app.utils.databases.utils import get_fields_from_model
from app.utils.enums.http_errors import CommonErrorMessages
from app.utils.enums.permission_enums import (AvailableOperations, AvailableServices)


async def modify_profile(profile_id: int, model: PydanticProfileModify, current_account: AccountInDB) -> None:
    """
    This method modifies the profile qualified by the id provided.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    academic_year: int = model.academic_year

    profile_to_modify: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)

    if profile_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    if await ProfileInDB.filter(mail=model.mail, academic_year=academic_year).exists():
        raise MailAlreadyUsedException

    if model.account_id is not None:
        if model.account_id != -1 and not await AccountInDB.filter(id=model.account_id).exists():
            raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND)

        # Helps ensuring that the account is not already assigned to another profile for the academic year provided.
        # The custom filters the current account from the query to avoid raising errors when modifying the current profile.
        q: Q = ~Q(id=profile_to_modify.id)
        if model.account_id != -1 and await ProfileInDB.filter(q,
                                                               account_id=model.account_id,
                                                               academic_year=academic_year).exists():
            raise HTTPException(status_code=409, detail=CommonErrorMessages.ACCOUNT_ALREADY_LINKED)

    if not await StatusInDB.filter(id=model.status_id).exists():
        raise HTTPException(status_code=404, detail=CommonErrorMessages.STATUS_NOT_FOUND)

    try:
        if model.account_id == -1:
            profile_to_modify.account_id = None
            model.account_id = None
        profile_to_modify.update_from_dict(model.model_dump(exclude_none=True))  # type: ignore
        await profile_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


async def create_profile(model: PydanticProfileCreate, current_account: AccountInDB) -> None:
    """
    This method creates a new profile.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.CREATE,
                            current_account)

    academic_year: int = model.academic_year

    #We check if the login or mail are already used
    if await ProfileInDB.filter(mail=model.mail, academic_year=academic_year).exists():
        raise MailAlreadyUsedException

    # We check if the account id is provided.
    # If so, we need to ensure that the account is not already assigned
    # to another profile for the academic year provided.
    if model.account_id is not None:
        if await ProfileInDB.filter(account_id=model.account_id,
                                    academic_year=academic_year).exists():
            raise HTTPException(status_code=409, detail=CommonErrorMessages.ACCOUNT_ALREADY_LINKED)
        if model.account_id != -1 and not await AccountInDB.filter(id=model.account_id).exists():
            raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND)

    if not await StatusInDB.filter(id=model.status_id).exists():
        raise HTTPException(status_code=404, detail=CommonErrorMessages.STATUS_NOT_FOUND)

    try:
        await ProfileInDB.create(
            firstname=model.firstname,
            lastname=model.lastname,
            mail=model.mail,
            academic_year=academic_year,
            quota=model.quota,
            account_id=model.account_id if model.account_id != -1 else None,
            status_id=model.status_id
        )
    except ValidationError as e:
        raise MailInvalidException from e


async def get_all_profiles(academic_year: int, current_account: AccountInDB, body: PydanticPagination) -> list[PydanticProfileResponse]:
    """
    Retrieves all profiles.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.GET, current_account)

    valid_fields : dict[str, Any] = get_fields_from_model(ProfileInDB)
    order_field  : str = body.order_by.lstrip('-')

    if order_field not in valid_fields:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COLUMN_DOES_NOT_EXIST.value)

    profiles_query: QuerySet[ProfileInDB] = ProfileInDB.filter(academic_year=academic_year).all()

    paginated_profile: list[ProfileInDB] = await body.paginate_query(profiles_query)
    return [PydanticProfileResponse.model_validate(profile) for profile in
            paginated_profile]  # Use model_validate for each profile


async def get_profile_by_id(profile_id: int, current_account: AccountInDB) -> PydanticProfileResponse:
    """
    Retrieves a profile by their ID.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.GET, current_account)

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    return PydanticProfileResponse.model_validate(profile)  # Use model_validate to create the response model


async def get_profiles_not_linked_to_account(academic_year: int, current_account: AccountInDB,body : PydanticPagination) -> list[PydanticProfileResponse]:
    """
    Retrieves all profiles not linked to an account.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    valid_fields: dict[str, Any] = get_fields_from_model(ProfileInDB)
    order_field: str = body.order_by.lstrip('-')

    if order_field not in valid_fields:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COLUMN_DOES_NOT_EXIST.value)

    profiles_query: QuerySet[ProfileInDB] = ProfileInDB.filter(account=None,academic_year=academic_year).all()

    paginated_profile: list[ProfileInDB] = await body.paginate_query(profiles_query)

    return [PydanticProfileResponse.model_validate(profile) for profile in paginated_profile]



async def get_current_profile(current_account: AccountInDB) -> PydanticProfileResponse:
    """
    Retrieves the current profile.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(account=current_account.id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    return PydanticProfileResponse.model_validate(profile)


async def search_profile_by_keywords(keywords: str, academic_year: int, current_account: AccountInDB, body: PydanticPagination) -> list[PydanticProfileResponse]:
    """
    Searches for a profile by keywords.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    valid_fields : dict[str, Any] = get_fields_from_model(ProfileInDB)
    order_field  : str = body.order_by.lstrip('-')

    if order_field not in valid_fields:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.COLUMN_DOES_NOT_EXIST.value)

    query: Q = Q()
    for keyword in keywords.split(" "):
        query &= (
                Q(lastname__icontains=keyword) |
                Q(firstname__icontains=keyword) |
                Q(mail__icontains=keyword)
        )

    profiles_query: QuerySet[ProfileInDB] = ProfileInDB.filter(query, academic_year=academic_year).all()

    profiles: list[ProfileInDB] = await body.paginate_query(profiles_query)

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


async def get_number_of_profile(academic_year: int, current_account: AccountInDB) -> PydanticNumberOfProfile:
    """
    This method get the number of profile.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    number_profile_with_account: int = await ProfileInDB.filter(academic_year=academic_year).exclude(account_id=None).count()

    number_profile_without_account: int = await ProfileInDB.filter(academic_year=academic_year, account_id=None).count()

    return PydanticNumberOfProfile(
        number_of_profiles_without_account=number_profile_without_account,
        number_of_profiles_with_account=number_profile_with_account
    )


async def alerte_profile(academic_year: int, current_account: AccountInDB) -> list[PydanticProfileResponse]:
    """
    This methode get the alert of the UE with a wrong number of affected hours
    """

    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    profiles_alert : list[PydanticProfileResponse] = []

    profiles : list[ProfileInDB] = await ProfileInDB.filter(academic_year=academic_year).all()

    for profile in profiles:
        profile_affectation : list[AffectationInDB] = await AffectationInDB.filter(profile_id=profile.id).all()
        sum_hours_affected: int = 0
        for affectation in profile_affectation:
            sum_hours_affected += affectation.hours
        if sum_hours_affected != profile.quota:
            profiles_alert.append(PydanticProfileResponse.model_validate(profile))

    return profiles_alert
