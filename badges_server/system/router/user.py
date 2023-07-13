from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from badges_server.config import logrdata
from badges_server.database.objs import Access, User
from badges_server.system.auth import dep_user
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.user import UserCreateModel, UserModel, UserResult

router = APIRouter(prefix="/users")


@router.get("/{id}", response_model=UserResult, tags=["users"])
async def select_user(id: int, db_async_session: AsyncSession = Depends(dep_db_async_session)):
    """
    Return the user with the specified ID.
    """
    query = select(User).filter_by(id=id).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(HTTP_404_NOT_FOUND)
    print(user_data.username)
    return {"action": "get", "user": user_data}


@router.post("", status_code=HTTP_201_CREATED, response_model=UserResult, tags=["users"])
async def create_user(
    data: UserCreateModel,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Create a user with the requested attributes.
    """
    if not user.headuser:
        raise HTTPException(HTTP_403_FORBIDDEN)
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
        raise HTTPException(HTTP_409_CONFLICT, str(expt))
    user_result = UserModel.from_orm(made_user).dict()
    uuidcode = uuid4().hex
    made_access = Access(
        user_id=UserModel.from_orm(made_user).id, code=uuidcode, active=True, uuid=uuidcode[0:4]
    )
    db_async_session.add(made_access)
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, str(expt))
    await db_async_session.flush()
    return {"action": "post", "user": user_result}
