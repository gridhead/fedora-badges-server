from sqlalchemy import select
from sqlalchemy.orm import selectinload

from badges_server.conf import logrdata
from badges_server.database.data import asynsess_generate
from badges_server.database.form.user import UserCreate_Parameter, UserPeruseSole_Parameter
from badges_server.database.intr import badgesdb
from badges_server.database.objs import User


class IntrUser:
    def __init__(self, badgesdb: badgesdb):
        self.relaname = "USER"
        self.sesclass = asynsess_generate
        self.sesclass.configure(bind=badgesdb.engnobjc)

    async def insert(self, objciden: UserCreate_Parameter):
        """
        Why sessobjc.commit() and why not sessobjc.flush() ?
        https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit
        """
        try:
            sessobjc = self.sesclass()
            try:
                datadict = {
                    "mailaddr": objciden.mailaddr,
                    "username": objciden.username,
                    "desc": objciden.desc,
                    "withdraw": objciden.withdraw,
                }
                dataobjc = User(**datadict)
                sessobjc.add(dataobjc)
                await sessobjc.commit()
                return True
            except Exception as expt:
                await sessobjc.rollback()
                logrdata.logrobjc.error(
                    f"Could not insert the record into the relation {self.relaname} - {expt}"
                )
                return False
        except Exception as expt:
            logrdata.logrobjc.error(
                f"Could not initialize a session with the relation {self.relaname} - {expt}"
            )
            return False

    async def peruse_sole(self, objciden: UserPeruseSole_Parameter):
        try:
            sessobjc = self.sesclass()
            quryobjc = select(User).filter_by(id=objciden.id).options(selectinload("*"))
            rsltobjc = await sessobjc.execute(quryobjc)
            await sessobjc.close()
            return rsltobjc.scalar_one_or_none()
        except Exception as expt:
            logrdata.logrobjc.error(
                f"Could not read one record from the relation {self.relaname} - {expt}"
            )
            return False

    def peruse_many(self):
        pass

    def update(self):
        pass

    def remove(self):
        pass
