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
from badges_server.system.models.user import (
    UserCreateModel,
    UserModelExternal,
    UserModelInternal,
    UserResult,
    UserUpdateActivityModel,
    UserUpdateDescriptionModel,
    UserUpdateEmailAddressModel,
    UserUpdatePermissionModel,
)

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
        desc=data.desc,
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
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    made_access = Access(
        user_id=UserModelInternal.from_orm(made_user).id,
        code=uuid4().hex,
        active=True,
        uuid=uuid4().hex[0:8],
    )
    db_async_session.add(made_access)
    user_result = UserModelExternal.from_orm(made_user).dict()
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    await db_async_session.flush()
    return {"action": "post", "user": user_result}


@router.put("/updateperm", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def update_permission(
    data: UserUpdatePermissionModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Update the permission level for the user with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(User).filter_by(uuid=data.uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{data.uuid}' was not found"
        )
    if user_data.withdraw:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"User with the requested UUID '{data.uuid}' have withdrawn from the service so their access levels cannot be modified",  # noqa: E501
        )
    if data.head:
        if user_data.headuser:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY,
                f"User with the requested UUID '{data.uuid}' already have the ADMIN access levels",
            )
        else:
            user_data.headuser = True
    if not data.head:
        if not user_data.headuser:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY,
                f"User with the requested UUID '{data.uuid}' does not have ADMIN access levels",
            )
        else:
            user_data.headuser = False
    await db_async_session.flush()
    return {"action": "put", "user": user_data}


@router.put("/updateactivity", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def update_activity(
    data: UserUpdateActivityModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Update the activity for the user accounts
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(User).filter_by(uuid=data.uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{data.uuid}' was not found"
        )
    if data.withdraw:
        if user_data.withdraw:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY,
                f"User with the requested UUID '{data.uuid}' have already withdrawn from the service",  # noqa: E501
            )
        else:
            user_data.withdraw = True
    if not data.withdraw:
        if not user_data.withdraw:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY,
                f"User with the requested UUID '{data.uuid}' have already enabled their account",
            )
        else:
            user_data.withdraw = False
    await db_async_session.flush()
    return {"action": "put", "user": user_data}


@router.put("/updatedesc", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def update_description(
    data: UserUpdateDescriptionModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Update the description of the user account with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(User).filter_by(uuid=data.uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{data.uuid}' was not found"
        )
    user_data.desc = data.desc
    await db_async_session.flush()
    return {"action": "put", "user": user_data}


@router.put("/updatemailaddr", status_code=HTTP_200_OK, response_model=UserResult, tags=["users"])
async def update_email_address(
    data: UserUpdateEmailAddressModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Update the email address of the user with the requested UUID
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    query = select(User).filter_by(uuid=data.uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{data.uuid}' was not found"
        )
    user_data.mailaddr = data.mailaddr
    await db_async_session.flush()
    return {"action": "put", "user": user_data}
