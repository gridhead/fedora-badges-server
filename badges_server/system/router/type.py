from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
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
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from badges_server.config import logrdata
from badges_server.database.objs import Type, User
from badges_server.system.auth import dep_user
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.type import (
    TypeCreateModel,
    TypeModelExternal,
    TypeResult,
    TypeUpdateDescriptionModel,
    TypeUpdateNameModel,
)

router = APIRouter(prefix="/types")


@router.get("/name/{name}", status_code=HTTP_200_OK, response_model=TypeResult, tags=["types"])
async def select_type_by_name(
    name: str, db_async_session: AsyncSession = Depends(dep_db_async_session)
):
    """
    Return the type with the specified name
    """
    query = select(Type).filter_by(name=name).options(selectinload("*"))
    result = await db_async_session.execute(query)
    type_data = result.scalar_one_or_none()
    if not type_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Type with the requested name '{name}' was not found"
        )
    return {"action": "get", "type": type_data}


@router.get("/uuid/{uuid}", status_code=HTTP_200_OK, response_model=TypeResult, tags=["types"])
async def select_user_by_uuid(
    uuid: str, db_async_session: AsyncSession = Depends(dep_db_async_session)
):
    """
    Return the type with the specified UUID
    """
    query = select(Type).filter_by(uuid=uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    type_data = result.scalar_one_or_none()
    if not type_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Type with the requested UUID '{uuid}' was not found"
        )
    return {"action": "get", "type": type_data}


@router.post("/create", status_code=HTTP_201_CREATED, response_model=TypeResult, tags=["types"])
async def create_type(
    data: TypeCreateModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Create a type with the requested attributes
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    made_type = Type(
        name=data.name,
        desc=data.desc,
        arranged=data.arranged,
        uuid=uuid4().hex[0:8],
    )
    db_async_session.add(made_type)
    type_result = TypeModelExternal.from_orm(made_type).dict()
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "post", "type": type_result}


@router.put("/updatename", status_code=HTTP_200_OK, response_model=TypeResult, tags=["types"])
async def update_name(
    data: TypeUpdateNameModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Update the name for the type with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(Type).filter_by(uuid=data.uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    type_data = result.scalar_one_or_none()
    if not type_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Type with the requested UUID '{data.uuid}' was not found"
        )
    if type_data.name == data.name:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"Type already has the same name '{data.name}' as requested for changing",
        )
    else:
        type_data.name = data.name
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "put", "type": type_data}


@router.put("/updatedesc", status_code=HTTP_200_OK, response_model=TypeResult, tags=["types"])
async def update_description(
    data: TypeUpdateDescriptionModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Update the description for the type with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(Type).filter_by(uuid=data.uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    type_data = result.scalar_one_or_none()
    if not type_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Type with the requested UUID '{data.uuid}' was not found"
        )
    if type_data.desc == data.desc:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"Type already has the same description '{data.desc}' as requested for changing",
        )
    else:
        type_data.desc = data.desc
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "put", "type": type_data}


@router.delete(
    "/uuid/{uuid}", status_code=HTTP_202_ACCEPTED, response_model=TypeResult, tags=["types"]
)
async def delete_type(
    uuid: str,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Delete the description for the type with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(Type).filter_by(uuid=uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    type_data = result.scalar_one_or_none()
    if not type_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Type with the requested UUID '{uuid}' was not found"
        )
    query = delete(Type).filter_by(id=type_data.id)
    await db_async_session.execute(query)
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "delete", "type": type_data}
