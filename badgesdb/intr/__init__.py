from badgesdb.data import make_sync_engine, syncsess_generate


class BadgesDBSync:
    def __init__(self, username, password, jsyncurl, dtbsport, database):
        self.username = username
        self.password = password
        self.jsyncurl = jsyncurl
        self.dtbspost = dtbsport
        self.database = database
        self.engnobjc = make_sync_engine(username, password, jsyncurl, dtbsport, database)
        self.syncsess = syncsess_generate.configure(bind=self.engnobjc)
