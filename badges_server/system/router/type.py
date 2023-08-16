from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_409_CONFLICT

from badges_server.config import logrdata
from badges_server.database.objs import Type, User
from badges_server.system.auth import dep_user
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.type import TypeCreateModel, TypeModelExternal, TypeResult

router = APIRouter(prefix="/types")


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
