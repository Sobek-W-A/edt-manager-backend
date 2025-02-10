"""
Profile-related operations service.
Provides the methods to use when interacting with a profile.
"""

from fastapi import HTTPException
from pydantic import ValidationError
from tortoise.expressions import Q
from tortoise.queryset import QuerySet

from app.models.pydantic.ProfileModel import (PydanticProfileCreate,
                                              PydanticProfileModify,
                                              PydanticProfileResponse)
from app.models.pydantic.tools.number_of_elements import NumberOfElement
from app.models.pydantic.tools.pagination import PydanticPagination
from app.models.tortoise.account import AccountInDB
from app.models.tortoise.profile import ProfileInDB
from app.models.tortoise.status import StatusInDB
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
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.UPDATE,
                            current_account)

    academic_year: int = 2024 # TODO: Change this to a URL parameter.


    profile_to_modify: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)

    if profile_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    if await ProfileInDB.filter(mail=model.mail, academic_year=academic_year).exists():
        raise MailAlreadyUsedException

    if model.account_id is not None:
        if not await AccountInDB.filter(id=model.account_id).exists():
            raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND)

        # Helps ensuring that the account is not already assigned to another profile for the academic year provided.
        # The custom filters the current account from the query to avoid raising errors when modifying the current profile.
        q: Q = ~Q(id=profile_to_modify.id)
        if await ProfileInDB.filter(q,
                                    account_id=model.account_id,
                                    academic_year=academic_year).exists():
            raise HTTPException(status_code=409, detail=CommonErrorMessages.ACCOUNT_ALREADY_LINKED)

    if not await StatusInDB.filter(id=model.status_id, academic_year=academic_year).exists():
        raise HTTPException(status_code=404, detail=CommonErrorMessages.STATUS_NOT_FOUND)

    try:
        profile_to_modify.update_from_dict(model.model_dump(exclude_none=True))    # type: ignore
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

    academic_year: int = 2024

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
        if not await AccountInDB.filter(id=model.account_id).exists():
            raise HTTPException(status_code=404, detail=CommonErrorMessages.ACCOUNT_NOT_FOUND)

    if not await StatusInDB.filter(id=model.status_id, academic_year=academic_year).exists():
        raise HTTPException(status_code=404, detail=CommonErrorMessages.STATUS_NOT_FOUND)

    try:
        await ProfileInDB.create(
            firstname=model.firstname,
            lastname=model.lastname,
            mail=model.mail,
            academic_year=academic_year,
            quota=model.quota,
            account_id=model.account_id,
            status_id=model.status_id
        )
    except ValidationError as e:
        raise MailInvalidException from e

async def get_all_profiles(current_account: AccountInDB, page:int, limit:int, order: str) -> list[PydanticProfileResponse]:
    """
    Retrieves all profiles.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.GET, current_account)

    body = PydanticPagination.model_validate({"page": page, "limit": limit, "order_by": order})

    valid_fields = ProfileInDB._meta.fields_map.keys()

    if order not in valid_fields:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.ORDER_DOES_NOT_EXIST.value)

    profiles_query: QuerySet[ProfileInDB] = ProfileInDB.all()

    paginated_profile: list[ProfileInDB] = await body.paginate_query(profiles_query)
    return [PydanticProfileResponse.model_validate(profile) for profile in paginated_profile]  # Use model_validate for each profile

async def get_profile_by_id(profile_id: int, current_account: AccountInDB) -> PydanticProfileResponse:
    """
    Retrieves a profile by their ID.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE, AvailableOperations.GET, current_account)

    profile: ProfileInDB | None = await ProfileInDB.get_or_none(id=profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    return PydanticProfileResponse.model_validate(profile)  # Use model_validate to create the response model

async def get_profiles_not_linked_to_account(academic_year: int, current_account: AccountInDB, body: PydanticPagination) -> list[PydanticProfileResponse]:
    """
    Retrieves all profiles not linked to an account.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    profiles: list[ProfileInDB] = await ProfileInDB.filter(account=None,
                                                           academic_year=academic_year).all()
    return [PydanticProfileResponse.model_validate(profile) for profile in profiles]

async def get_current_profile(current_account: AccountInDB) -> PydanticProfileResponse:
    """
    Retrieves the current profile.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    profile : ProfileInDB | None = await ProfileInDB.get_or_none(account=current_account.id)
    if profile is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.PROFILE_NOT_FOUND)

    return PydanticProfileResponse.model_validate(profile)

async def search_profile_by_keywords(keywords: str, current_account: AccountInDB, page: int, limit: int) -> list[PydanticProfileResponse]:
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
            Q(firstname__icontains=keyword) |
            Q(mail__icontains=keyword)
        )

    profiles: list[ProfileInDB] = await ProfileInDB.filter(query).all()

    start: int = (page - 1) * limit
    end: int = start + limit
    return [PydanticProfileResponse.model_validate(profile) for profile in profiles][start:end]

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


async def get_number_of_profile(academic_year: int, current_account: AccountInDB) -> NumberOfElement:
    """
    This method get the number of profile.
    """
    await check_permissions(AvailableServices.PROFILE_SERVICE,
                            AvailableOperations.GET,
                            current_account)

    number_profile: int = await ProfileInDB.filter(academic_year=academic_year).count()

    return NumberOfElement(
        number_of_elements=number_profile
    )
