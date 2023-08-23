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
from badges_server.database.objs import Accolade, Type, User
from badges_server.system.auth import dep_user
from badges_server.system.database import dep_db_async_session
from badges_server.system.models.accolade import (
    AccoladeCreateModel,
    AccoladeModelExternal,
    AccoladeResult,
)

router = APIRouter(prefix="/accolades")


@router.post(
    "/create", status_code=HTTP_201_CREATED, response_model=AccoladeResult, tags=["accolades"]
)
async def create_accolade(
    data: AccoladeCreateModel,
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
    query = select(Type).filter_by(uuid=data.type_uuid).options(selectinload("*"))
    result = await db_async_session.execute(query)
    type_data = result.scalar_one_or_none()
    if not type_data:
        raise HTTPException(
            HTTP_404_NOT_FOUND, f"Type with the requested UUID '{data.type_uuid}' was not found"
        )
    uuidtext = uuid4().hex[0:8]
    made_accolade = Accolade(
        name=data.name,
        desc=data.desc,
        imejdata=uuidtext,
        criteria=data.criteria,
        type_id=type_data.id,
        sequence=data.sequence,
        tags=data.tags,
        uuid=uuidtext,
    )
    db_async_session.add(made_accolade)
    accolade_result = AccoladeModelExternal.from_orm(made_accolade).dict()
    try:
        await db_async_session.flush()
    except IntegrityError as expt:
        logrdata.logrobjc.warning("Uniqueness constraint failed - Please try again")
        logrdata.logrobjc.warning(str(expt))
        raise HTTPException(HTTP_409_CONFLICT, "Uniqueness constraint failed - Please try again")
    return {"action": "post", "accolade": accolade_result}
