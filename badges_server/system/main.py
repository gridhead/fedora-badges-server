import copy

import uvicorn.config

from badges_server.config import logrdata, standard

from fastapi import FastAPI

from badges_server.database import data
from badges_server import interactions
from badges_server.exceptions import BadgesServerException

from badges_server import __vers__


desc = "Fedora Badges Server"


tags_metadata = [
    {"name": "accolade", "description": "Operations on accolades"},
    {"name": "granting", "description": "Operations on grantings"},
    {"name": "invitation", "description": "Operations on invitation"},
    {"name": "provider", "description": "Operations on providers"},
    {"name": "type", "description": "Operations on types"},
    {"name": "user", "description": "Operations on users"},
]

app = FastAPI(
    title="Fedora   Badges Server",
    description=desc,
    version=__vers__,
    contact={"name": "Fedora Infrastructure", "email": "infrastructure@lists.fedoraproject.org"},
    openapi_tags=tags_metadata,
)


PREFIX = "/api/v1"


def start_service():
    loglevel_string = standard.logrconf["handlers"]["console"]["level"]
    loglevel_number = uvicorn.config.LOG_LEVELS[loglevel_string.lower()]
    logrdata.logrobjc.info("Starting Badges Server ...")
    logrdata.logrobjc.info(f"Host address     : {standard.servhost}")
    logrdata.logrobjc.info(f"Port number      : {standard.servport}")
    logrdata.logrobjc.info(f"Log level        : {loglevel_string} / {loglevel_string}")
    logrdata.logrobjc.info(f"Reload on change : {str(standard.cgreload).upper()}")
    logrdata.logrobjc.info(f"Serving API docs on http://{standard.servhost}:{standard.servport}/docs")
    uvicorn.run(
        "badges_server.system.main:app",
        host=standard.servhost,
        port=standard.servport,
        log_level=loglevel_number,
        reload=standard.cgreload,
        log_config=standard.wsgiconf,
    )
