import os
from importlib import metadata
from logging import getLogger
from logging.config import dictConfig

from badges_server.config import logrdata, standard

__vers__ = metadata.version("badges_server")


def readconf():
    conffile = os.getenv("FSBS_CONFFILE")
    confdict = {}
    with open(conffile) as confobjc:
        exec(compile(confobjc.read(), conffile, "exec"), confdict)
    standard.database = confdict.get("database", standard.database)
    standard.jsyncurl = confdict.get("jsyncurl", standard.jsyncurl)
    standard.asyncurl = confdict.get("asyncurl", standard.asyncurl)
    standard.dtbsport = confdict.get("dtbsport", standard.dtbsport)
    standard.username = confdict.get("username", standard.username)
    standard.password = confdict.get("password", standard.password)
    standard.servhost = confdict.get("servhost", standard.servhost)
    standard.servport = confdict.get("servport", standard.servport)
    standard.cgreload = confdict.get("cgreload", standard.cgreload)
    standard.wsgiconf = confdict.get("wsgiconf", standard.wsgiconf)
    dictConfig(standard.logrconf)
    logrdata.logrobjc = getLogger(__name__)
    logrdata.logrobjc.info("Reading the configuration again")
