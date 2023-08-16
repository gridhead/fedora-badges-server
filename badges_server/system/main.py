import sys

import uvicorn.config
from fastapi import FastAPI

from badges_server import __vers__, readconf
from badges_server.config import logrdata, standard
from badges_server.database import data
from badges_server.exceptions import BadgesServerConfigurationError
from badges_server.system.router import access, type, user

desc = "Fedora Badges Server"


tags_metadata = [
    {"name": "accesses", "description": "Operations on accesses"},
    {"name": "accolades", "description": "Operations on accolades"},
    {"name": "grantings", "description": "Operations on grantings"},
    {"name": "invitations", "description": "Operations on invitation"},
    {"name": "providers", "description": "Operations on providers"},
    {"name": "types", "description": "Operations on types"},
    {"name": "users", "description": "Operations on users"},
]

app = FastAPI(
    title="Fedora Badges Server",
    description=desc,
    version=__vers__,
    contact={"name": "Fedora Infrastructure", "email": "infrastructure@lists.fedoraproject.org"},
    openapi_tags=tags_metadata,
)


PREFIX = "/api/v1"

app.include_router(user.router, prefix=PREFIX)
app.include_router(access.router, prefix=PREFIX)
app.include_router(type.router, prefix=PREFIX)


@app.on_event("startup")
async def init_model():
    try:
        readconf()
        data.init_sync_model()
        await data.init_async_model()
    except BadgesServerConfigurationError:
        logrdata.logrobjc.error("Configuration file needs attention")
        sys.exit(1)


def start_service():
    loglevel_string = standard.logrconf["handlers"]["console"]["level"]
    loglevel_number = uvicorn.config.LOG_LEVELS[loglevel_string.lower()]
    logrdata.logrobjc.info("Starting Badges Server ...")
    logrdata.logrobjc.info(f"Host address     : {standard.servhost}")
    logrdata.logrobjc.info(f"Port number      : {standard.servport}")
    logrdata.logrobjc.info(f"Log level        : {loglevel_string} / {loglevel_string}")
    logrdata.logrobjc.info(f"Reload on change : {str(standard.cgreload).upper()}")
    logrdata.logrobjc.info(
        f"Serving API docs on http://{standard.servhost}:{standard.servport}/docs"
    )
    uvicorn.run(
        "badges_server.system.main:app",
        host=standard.servhost,
        port=standard.servport,
        log_level=loglevel_number,
        reload=standard.cgreload,
        log_config=standard.wsgiconf,
    )
