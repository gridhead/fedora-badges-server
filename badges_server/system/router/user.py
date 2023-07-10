from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from sqlalchemy.orm import selectinload
from badges_server.config import logrdata
from badges_server.system.models import user as user_model
from sqlalchemy.ext.asyncio import AsyncSession
from badges_server.system.database import dep_db_async_session
from badges_server.database.objs import User
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)


router = APIRouter(prefix="/users")

@router.get("/{id}", response_model=user_model.SelectOne, tags=["users"])
async def select_user(id: int, db_async_session: AsyncSession = Depends(dep_db_async_session)):
    """
    Return the user with the specified ID.
    """
    query = select(User).filter_by(id=id).options(selectinload("*"))
    result = await db_async_session.execute(query)
    user_data = result.scalar_one_or_none()

    if not user_data:
        raise HTTPException(HTTP_404_NOT_FOUND)

    return {"action": "get", "user": user_data}
