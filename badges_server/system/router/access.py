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
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from badges_server.config import logrdata
from badges_server.database.objs import Access, User
from badges_server.database.util import utcnow
from badges_server.system.auth import dep_user
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.access import AccessModel, AccessResult

router = APIRouter(prefix="/accesses")


@router.post(
    "/reload/{uuid}", status_code=HTTP_201_CREATED, response_model=AccessResult, tags=["accesses"]
)
async def reload_access_code(
    uuid: str,
    db_async_session: AsyncSession = Depends(dep_db_async_session),
    user: User = Depends(dep_user),
):
    """
    Invalidate the existing active access code and generate a new one in its place
    """
    if not user.headuser:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            "Access to this endpoint is now allowed for users with inadequate access levels",
        )
    user_query = select(User).filter_by(uuid=uuid).options(selectinload("*"))
    user_result = await db_async_session.execute(user_query)
    user_data = user_result.scalar_one_or_none()
    if not user_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"User with the requested UUID '{uuid}' was not found"
        )
    if user_data.withdraw:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            f"User with the requested UUID '{uuid}' have withdrawn from the service so their access levels cannot be modified",  # noqa: E501
        )
    access_query = (
        select(Access).filter_by(user_id=user_data.id, active=True).options(selectinload("*"))
    )
    access_result = await db_async_session.execute(access_query)
    access_data = access_result.scalar_one_or_none()
    access_data.stopdate = utcnow()
    access_data.active = False
    update_access = Access(
        user_id=user_data.id,
        code=uuid4().hex,
        active=True,
        uuid=uuid4().hex[0:8],
    )
    db_async_session.add(update_access)
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "post", "access": AccessModel.from_orm(update_access).dict()}
