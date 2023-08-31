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
    HTTP_202_ACCEPTED,
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
from badges_server.system.models.accolade import (
    AccoladeModelExternal,
    AccoladeResult,
    AccoladeSearchResult,
    AccoladeSingleTypeSearchResult,
    AccoladeUpdateNameModel,
)

router = APIRouter(prefix="/accolades")


@router.get(
    "/search/{text}",
    status_code=HTTP_200_OK,
    response_model=AccoladeSearchResult,
    tags=["accolades"],
)
async def search_by_text(text: str, db_async_session: AsyncSession = Depends(dep_db_async_session)):
    """
    Return the results from searching accolades with the specified text
    """

    """
    TODO: Implement a proper full-text search instead of
        the makeshift approach using the SQL LIKE clause
    """

    query_name = select(Accolade).filter(Accolade.name.like(f"%{text}%")).options(selectinload("*"))
    result_name = await db_async_session.execute(query_name)
    data_name = result_name.scalars().fetchall()
    objc_name = AccoladeSingleTypeSearchResult()
    objc_name.quantity, objc_name.result = len(data_name), data_name

    query_desc = select(Accolade).filter(Accolade.desc.like(f"%{text}%")).options(selectinload("*"))
    result_desc = await db_async_session.execute(query_desc)
    data_desc = result_desc.scalars().fetchall()
    objc_desc = AccoladeSingleTypeSearchResult()
    objc_desc.quantity, objc_desc.result = len(data_desc), data_desc

    query_tags = select(Accolade).filter(Accolade.tags.like(f"%{text}%")).options(selectinload("*"))
    result_tags = await db_async_session.execute(query_tags)
    data_tags = result_tags.scalars().fetchall()
    objc_tags = AccoladeSingleTypeSearchResult()
    objc_tags.quantity, objc_tags.result = len(data_tags), data_tags

    quantity = len(data_name) + len(data_desc) + len(data_tags)
    if quantity == 0:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Accolades with the substring '{text}' were not found"
        )

    result = AccoladeSearchResult()
    result.action, result.quantity, result.match_name, result.match_desc, result_tags = (
        "get",
        quantity,
        objc_name,
        objc_desc,
        objc_tags,
    )
    return result


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
    accolade_data = result.scalar_one_or_none()
    if not accolade_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Accolade with the requested UUID '{uuid}' was not found"
        )
    return {"action": "get", "accolade": accolade_data}


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


@router.put(
    "/updatename/", status_code=HTTP_202_ACCEPTED, response_model=AccoladeResult, tags=["accolades"]
)
async def update_name(
    data: AccoladeUpdateNameModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Update the name for the accolade with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(Accolade).filter_by(uuid=data.uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    accolade_data = result.scalar_one_or_none()
    if not accolade_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Accolade with the requested UUID '{data.uuid}' was not found"
        )
    if accolade_data.name == data.name:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"Accolade already has the same name '{data.name}' as requested for changing",
        )
    accolade_data.name = data.name
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "put", "accolade": accolade_data}
