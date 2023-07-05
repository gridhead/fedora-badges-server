from importlib import metadata
from logging import getLogger
from logging.config import dictConfig

from badges_server.conf import logrdata, standard

__vers__ = metadata.version("badges_server")


def readconf(confobjc):
    standard.database = confobjc.get("database", standard.database)
    standard.jsyncurl = confobjc.get("jsyncurl", standard.jsyncurl)
    standard.asyncurl = confobjc.get("asyncurl", standard.asyncurl)
    standard.dtbsport = confobjc.get("dtbsport", standard.dtbsport)
    standard.username = confobjc.get("username", standard.username)
    standard.password = confobjc.get("password", standard.password)
    dictConfig(standard.logrconf)
    logrdata.logrobjc = getLogger(__name__)
