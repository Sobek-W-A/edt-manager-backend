"""
This module provides the FolderPydanticModel class.
"""
from fastapi import HTTPException
from typing import Optional, List

from app.models.pydantic.AcademicYearModel import AcademicYearPydanticModel
from app.models.pydantic.UEModel import PydanticUEModel
from app.utils.enums.http_errors import CommonErrorMessages


class PydanticFolderModel(AcademicYearPydanticModel):
    name: str
    children: Optional[List["PydanticFolderModel"]] = None
    ue: Optional[PydanticUEModel] = None

    def validate_children_or_ue (cls,value):
        children = value.get("children")
        ue = value.get("ue")

        if children and ue:
            raise HTTPException(status_code=422, detail=CommonErrorMessages.FOLDER_AND_UE_NOT_ENABLED)

        return value

    class Config:
        #allow to use self reference in type
        arbitrary_types_allowed = True


PydanticFolderModel.update_forward_refs()
