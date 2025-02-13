"""
Account Endpoints.
"""

from fastapi import APIRouter, Response

from app.models.aliases import AuthenticatedAccount
from app.models.pydantic.AccountModel import (PydanticAccountModel,
                                              PydanticAccountPasswordResponse, PydanticAccountWithoutProfileModel,
                                              PydanticCreateAccountModel,
                                              PydanticModifyAccountModel)

from app.models.pydantic.PydanticRole import (PydanticRoleResponseModel,
                                              PydanticSetRoleToAccountModel)
from app.models.pydantic.tools.number_of_elements import NumberOfElement
from app.routes.tags import Tag
from app.services import AccountService

accountRouter: APIRouter = APIRouter(prefix="/account")
tag: Tag = {
    "name": "Account",
    "description": "Account-related operations."
}


@accountRouter.get("/", status_code=200, response_model=list[PydanticAccountModel])
async def get_all_accounts(academic_year: int, current_account: AuthenticatedAccount) -> list[PydanticAccountModel]:
    """
    This method returns all the accounts.
    """
    return await AccountService.get_all_accounts(academic_year, current_account)


@accountRouter.get("/notlinkedtoprofile", status_code=200,
                   response_model=list[PydanticAccountWithoutProfileModel])
async def get_accounts_not_linked_to_profile(academic_year: int, current_account: AuthenticatedAccount) -> list[
    PydanticAccountWithoutProfileModel]:
    """
    This method returns all the accounts not linked to a profile.
    It returns specifically accounts that are not linked to a profile ever,
    or for the given academic year.
    """
    return await AccountService.get_accounts_not_linked_to_profile(academic_year, current_account)


@accountRouter.get("/{account_id}", status_code=200, response_model=PydanticAccountModel)
async def get_account(academic_year: int, account_id: int, current_account: AuthenticatedAccount) -> PydanticAccountModel:
    """
    This method returns an account by its ID.
    """
    return await AccountService.get_account(academic_year, account_id, current_account)


@accountRouter.post("/", status_code=201, response_model=PydanticAccountPasswordResponse)
async def create_account(account: PydanticCreateAccountModel,
                         current_account: AuthenticatedAccount) -> PydanticAccountPasswordResponse:
    """
    This method creates an account.
    """
    return await AccountService.create_account(account, current_account)


@accountRouter.patch("/{account_id}", status_code=205)
async def modify_account(account_id: int, account: PydanticModifyAccountModel,
                         current_account: AuthenticatedAccount) -> Response:
    """
    This method modifies an account.
    """
    await AccountService.modify_account(account_id, account, current_account)

    return Response(status_code=205)


@accountRouter.delete("/{account_id}", status_code=204)
async def delete_account(account_id: int, current_account: AuthenticatedAccount) -> None:
    """
    This method deletes an account.
    """
    await AccountService.delete_account(account_id, current_account)


@accountRouter.get("/{account_id}/role", status_code=200, response_model=PydanticRoleResponseModel)
async def get_role_account_by_id(account_id: int, academic_year: int,
                                 current_account: AuthenticatedAccount) -> PydanticRoleResponseModel:
    """
    This method get an account's roles with the account ID.
    """

    return await AccountService.get_role_account_by_id(account_id, current_account, academic_year)


@accountRouter.get("/search/login/{keywords}", status_code=200, response_model=list[PydanticAccountModel])
async def search_account_by_login(academic_year: int, keywords: str, current_account: AuthenticatedAccount) -> list[PydanticAccountModel]:
    """
    This method search an account by login.
    """

    return await AccountService.search_accounts_by_login(academic_year, keywords, current_account)


@accountRouter.get("/search/{keywords}", status_code=200, response_model=list[PydanticAccountModel])
async def search_account_by_keywords(academic_year: int, keywords: str, current_account: AuthenticatedAccount) -> list[
    PydanticAccountModel]:
    """
    This method search an account by keywords.
    """

    return await AccountService.search_account_by_keywords(academic_year, keywords, current_account)


@accountRouter.patch("/{account_id}/role/", status_code=205)
async def set_role_account_by_id(account_id: int, current_account: AuthenticatedAccount,
                                 body: PydanticSetRoleToAccountModel) -> Response:
    """
    This method set an account's roles with the account ID and a body.
    """
    await AccountService.set_role_account_by_name(account_id, current_account, body)

    return Response(status_code=205)


@accountRouter.get("/nb/", status_code=200, response_model=NumberOfElement)
async def get_nb_accounts(current_account: AuthenticatedAccount) -> NumberOfElement:
    """
    This method get the number of account in the database.
    """
    return await AccountService.get_number_of_account(current_account)
