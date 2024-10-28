
from fastapi import HTTPException
from app.models.pydantic.UserModel import PydanticUserModify, PydanticUserResponse
from app.models.tortoise.user import UserInDB
from app.utils.http_errors import CommonErrorMessages


async def modify_user(user_id: int, model: PydanticUserModify) -> PydanticUserResponse:
    user_to_modify: UserInDB | None = await UserInDB.get_or_none(id=user_id)

    if user_to_modify is None:
        raise HTTPException(status_code=404, detail=CommonErrorMessages.USER_NOT_FOUND)
    
    try:

        user_to_modify.update_from_dict(model.model_dump(exclude={"password", "password_confirm"})) # type: ignore
        if model.password is not None:
            user_to_modify.hash = UserInDB.get_password_hash(model.password)
        await user_to_modify.save()

    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    
    return PydanticUserResponse(
        id=user_to_modify.id,
        login=user_to_modify.login,
        firstname=user_to_modify.firstname,
        lastname=user_to_modify.lastname,
        mail=user_to_modify.mail
    )