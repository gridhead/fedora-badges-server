# from badgesdb.data import asynsess_generate
from badgesdb import data
from badgesdb.data import make_sync_engine


class BadgesDB:
    def __init__(self, username, password, jsyncurl, dtbsport, database):
        self.username = username
        self.password = password
        self.jsyncurl = jsyncurl
        self.dtbspost = dtbsport
        self.database = database
        self.engnobjc = make_sync_engine(username, password, jsyncurl, dtbsport, database)
        self.sessobjc = data.syncsess_generate.configure(bind=self.engnobjc)  # NEEDS ATTENTION
