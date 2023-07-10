from importlib import metadata
from logging import getLogger
from logging.config import dictConfig

from badges_server.config import logrdata, standard

__vers__ = metadata.version("badges_server")


def readconf(confobjc):
    standard.database = confobjc.get("database", standard.database)
    standard.jsyncurl = confobjc.get("jsyncurl", standard.jsyncurl)
    standard.asyncurl = confobjc.get("asyncurl", standard.asyncurl)
    standard.dtbsport = confobjc.get("dtbsport", standard.dtbsport)
    standard.username = confobjc.get("username", standard.username)
    standard.password = confobjc.get("password", standard.password)
    standard.servhost = confobjc.get("servhost", standard.servhost)
    standard.servport = confobjc.get("servport", standard.servport)
    standard.cgreload = confobjc.get("cgreload", standard.cgreload)
    standard.wsgiconf = confobjc.get("wsgiconf", standard.wsgiconf)
    dictConfig(standard.logrconf)
    logrdata.logrobjc = getLogger(__name__)
