from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_404_NOT_FOUND

from badges_server.database.objs import User
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.user import SelectOneResult

router = APIRouter(prefix="/users")


@router.get("/{id}", response_model=SelectOneResult, tags=["users"])
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
