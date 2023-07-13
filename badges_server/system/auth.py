from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from badges_server.database.objs import Access, User
from badges_server.system.database import dep_db_async_session


def dep_user_factory(optional: bool = False, **kwargs):
    """
    Factory creating FastAPI dependencies for authenticating users
    """
    if optional:
        kwargs["auto_error"] = False
    security = HTTPBasic(realm="badges_server", **kwargs)

    async def dep_user_actual(
        db_async_session: AsyncSession = Depends(dep_db_async_session),
        cred: HTTPBasicCredentials = Security(security),
    ):
        if not cred:
            if not optional:
                raise HTTPException(HTTP_403_FORBIDDEN)
            else:
                return None
        username = cred.username
        password = cred.password
        # query = select(User).filter_by(username=username)
        # result = await db_async_session.execute(query)
        # userdata = result.scalar_one_or_none()

        userdata = (
            await db_async_session.execute(select(User).filter_by(username=username))
        ).scalar_one_or_none()

        if userdata.withdraw:
            raise HTTPException(HTTP_401_UNAUTHORIZED)
        if not userdata:
            raise HTTPException(HTTP_401_UNAUTHORIZED)

        passdata = (
            await db_async_session.execute(
                select(Access).filter_by(user_id=userdata.id, name="BDGS_ACCESS")
            )
        ).scalar_one_or_none()

        if not passdata:
            raise HTTPException(HTTP_401_UNAUTHORIZED)
        if passdata.code != password:
            raise HTTPException(HTTP_403_FORBIDDEN)
        return userdata

    return dep_user_actual


dep_user = dep_user_factory()
dep_user_optional = dep_user_factory(optional=True)
