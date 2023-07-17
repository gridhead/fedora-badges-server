from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
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
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from badges_server.config import logrdata
from badges_server.database.objs import Access, User
from badges_server.system.auth import dep_user
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.user import UserCreateModel, UserModel, UserResult

router = APIRouter(prefix="/users")


@router.get(
    "/username/{username}", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"]
)
async def select_user_by_username(
    username: str, db_async_session: AsyncSession = Depends(dep_db_async_session)
):
    """
    Return the user with the specified username
    """
    query = select(User).filter_by(username=username).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested username '{username}' was not found"
        )
    return {"action": "get", "user": user_data}


@router.get("/uuid/{uuid}", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def select_user_by_uuid(
    uuid: str, db_async_session: AsyncSession = Depends(dep_db_async_session)
):
    """
    Return the user with the specified UUID
    """
    query = select(User).filter_by(uuid=uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{uuid}' was not found"
        )
    return {"action": "get", "user": user_data}


@router.post("/create", status_code=HTTP_201_CREATED, response_model=UserResult, tags=["users"])
async def create_user(
    data: UserCreateModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Create a user with the requested attributes
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    made_user = User(
        username=data.username,
        mailaddr=data.mailaddr,
        description=data.description,
        withdraw=False,
        headuser=False,
        uuid=uuid4().hex[0:8],
    )
    db_async_session.add(made_user)
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(
            HTTP_409_CONFLICT, f"Uniqueness constraint failed - Please try again - {str(expt)}"
        )
    made_access = Access(
        user_id=UserModel.from_orm(made_user).id,
        code=uuid4().hex,
        active=True,
        uuid=uuid4().hex[0:8],
    )
    db_async_session.add(made_access)
    user_result = UserModel.from_orm(made_user).dict()
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(
            HTTP_409_CONFLICT, f"Uniqueness constraint failed - Please try again - {str(expt)}"
        )
    await db_async_session.flush()
    return {"action": "post", "user": user_result}


@router.put("/promote", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def promote_user_access_level(
    uuid: str,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Promote the access level for the user with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(User).filter_by(uuid=uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{uuid}' was not found"
        )
    if user_data.withdraw:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"User with the requested UUID '{uuid}' have withdrawn from the service",
        )
    if user_data.headuser:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"User with the requested UUID '{uuid}' already have the ADMIN access levels",
        )
    user_data.headuser = True
    await db_async_session.flush()
    return {"action": "put", "user": user_data}


@router.put("/demote", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def demote_user_access_level(
    uuid: str,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Demote the access level for the user with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(User).filter_by(uuid=uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{uuid}' was not found"
        )
    if user_data.withdraw:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"User with the requested UUID '{uuid}' have withdrawn from the service",
        )
    if not user_data.headuser:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"User with the requested UUID '{uuid}' does not have ADMIN access levels",
        )
    user_data.headuser = False
    await db_async_session.flush()
    return {"action": "put", "user": user_data}
