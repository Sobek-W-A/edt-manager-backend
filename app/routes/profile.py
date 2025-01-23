"""
This module provieds a router for the /Profile endpoint.
"""
from fastapi import APIRouter, Response

from app.models.pydantic.ProfileModel import (PydanticProfileModify,
                                              PydanticProfileCreate,
                                              PydanticProfileResponse, PydanticNumberOfProfile)
from app.models.aliases import AuthenticatedAccount
from app.routes.tags import Tag
from app.services import ProfileService

profileRouter: APIRouter = APIRouter(prefix="/profile")
tag: Tag = {
    "name": "Profile",
    "description": "Profile-related operations."
}

@profileRouter.post("/", status_code=201)
async def create_profile(body: PydanticProfileCreate, current_account: AuthenticatedAccount) -> None:
    """
    This method creates a new Profile
    and return his password.
    """
    await ProfileService.create_profile(body, current_account)


@profileRouter.patch("/{profile_id}", status_code=205)
async def modify_profile(profile_id: int, profile_model: PydanticProfileModify, current_account: AuthenticatedAccount) -> Response:
    """
    This controllers is used when modifying Profile informations.
    """
    await ProfileService.modify_profile(profile_id, profile_model, current_account)
    return Response(status_code=205)


@profileRouter.get("/", response_model=list[PydanticProfileResponse], status_code=200)
async def get_all_profiles(current_account: AuthenticatedAccount) -> list[PydanticProfileResponse]:
    """
    Retrieves a list of all Profiles.
    """
    return await ProfileService.get_all_profiles(current_account)

@profileRouter.get("/me", response_model=PydanticProfileResponse, status_code=200)
async def get_current_profile(current_account: AuthenticatedAccount) -> PydanticProfileResponse:
    """
    Retrieves data from the currently connected Profile.
    """
    return await ProfileService.get_current_profile(current_account)

@profileRouter.get("/notlinked/{academic_year}", response_model=list[PydanticProfileResponse], status_code=200)
async def get_profiles_not_linked_to_account(academic_year: int, current_account: AuthenticatedAccount) -> list[PydanticProfileResponse]:
    """
    Returns all the profiles that are not linked to an account for the given academic year.
    """
    return await ProfileService.get_profiles_not_linked_to_account(academic_year, current_account)

@profileRouter.get("/{profile_id}", response_model=PydanticProfileResponse, status_code=200)
async def get_profile_by_id(profile_id: int, current_account: AuthenticatedAccount) -> PydanticProfileResponse:
    """
    Retrieves a Profile by their ID.
    """
    return await ProfileService.get_profile_by_id(profile_id, current_account)

@profileRouter.get("/search/{keywords}", response_model=list[PydanticProfileResponse], status_code=200)
async def search_profile(keywords: str, current_account: AuthenticatedAccount) -> list[PydanticProfileResponse]:
    """
    This method retrieves profiles that matches the keywords provided.
    """
    return await ProfileService.search_profile_by_keywords(keywords, current_account)


@profileRouter.delete("/{profile_id}", status_code=204)
async def delete_profile(profile_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This route is used for deleting a Profile
    """
    await ProfileService.delete_profile(profile_id, current_account)

@profileRouter.get("/nb/", status_code=200,response_model=PydanticNumberOfProfile)
async def get_nb_profile(current_account: AuthenticatedAccount) -> PydanticNumberOfProfile:
    """
    This method get the number of profile in the database.
    """
    return await ProfileService.get_number_of_profile(current_account)
