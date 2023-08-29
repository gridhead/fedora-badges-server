from os.path import exists, join
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_424_FAILED_DEPENDENCY,
)

from badges_server.config import logrdata, standard
from badges_server.database.objs import Accolade, Type, User
from badges_server.system.auth import dep_user
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.accolade import AccoladeModelExternal, AccoladeResult

router = APIRouter(prefix="/accolades")


@router.get(
    "/file/{uuid}", status_code=HTTP_200_OK, response_class=FileResponse, tags=["accolades"]
)
async def show_file_by_uuid(
    uuid: str, db_async_session: AsyncSession = Depends(dep_db_async_session)
):
    """
    Return the file for the accolade with the specified UUID
    """
    query = select(Accolade).filter_by(uuid=uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    accolade_data = result.scalar_one_or_none()
    if not accolade_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Accolade with the requested UUID '{uuid}' was not found"
        )
    filepath = join(standard.drctloca, f"{accolade_data.uuid}.png")
    if not exists(filepath):
        raise HTTPException(
            HTTP_424_FAILED_DEPENDENCY,
            f"File assets for the accolade with the requested UUID '{uuid}' was not found on the storage device",  # noqa: E501
        )
    return FileResponse(filepath)


@router.get(
    "/uuid/{uuid}", status_code=HTTP_200_OK, response_model=AccoladeResult, tags=["accolades"]
)
async def select_accolade_by_uuid(
    uuid: str, db_async_session: AsyncSession = Depends(dep_db_async_session)
):
    """
    Return the accolade with the specified UUID
    """
    query = select(Accolade).filter_by(uuid=uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Accolade with the requested UUID '{uuid}' was not found"
        )
    return {"action": "get", "accolade": user_data}


@router.post(
    "/create", status_code=HTTP_201_CREATED, response_model=AccoladeResult, tags=["accolades"]
)
async def create_accolade(
    name: Annotated[str, Form()],
    type_uuid: Annotated[str, Form()],
    file: UploadFile,
    desc: Annotated[str, Form()] = "",
    criteria: Annotated[str, Form()] = "",
    sequence: Annotated[int, Form()] = 0,
    tags: Annotated[str, Form()] = "",
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Create an accolade with the requested attributes
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    if file.size > standard.upslimit * 1024 * 1024:
        raise HTTPException(
            HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"The size of the uploaded asset exceeds the storage limit of {standard.upslimit} MiB",
        )
    if file.content_type != standard.conttype:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            "The content type of the uploaded asset does not match the accepted content type",
        )
    query = select(Type).filter_by(uuid=type_uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    type_data = result.scalar_one_or_none()
    if not type_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Type with the requested UUID '{type_uuid}' was not found"
        )
    uuidtext = uuid4().hex[0:8]
    made_accolade = Accolade(
        name=name,
        desc=desc,
        imageurl=uuidtext,
        criteria=criteria,
        type_id=type_data.id,
        sequence=sequence,
        tags=tags,
        uuid=uuidtext,
    )
    db_async_session.add(made_accolade)
    accolade_result = AccoladeModelExternal.from_orm(made_accolade).dict()
    """
    TODO: Check with the repository to ensure the existence of the `criteria`
    TODO: Confirm if the badges pushed are INDEED existing in the `collections` repository
    """
    try:
        await db_async_session.flush()
        with open(join(standard.drctloca, f"{uuidtext}.png"), "wb") as fileobjc:
            fileobjc.write(file.file.read())
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "post", "accolade": accolade_result}
