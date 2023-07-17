from typing import Set

from alembic import command, config, runtime, script
from sqlalchemy import URL

from badges_server.config import logrdata, standard
from badges_server.database.data.formatdb import migrpath


class AlembicMigration:
    @property
    def config(self):
        if not hasattr(self, "_config"):
            self._config = config.Config()
            self._config.set_main_option("script_location", migrpath)
            self._config.set_main_option(
                "sqlalchemy.url",
                URL.create(
                    "postgresql+psycopg2",
                    username=standard.username,
                    password=standard.password,
                    host=standard.jsyncurl,
                    port=standard.dtbsport,
                    database=standard.database,
                )
                .render_as_string(hide_password=False)
                .replace("%", "%%"),
            )
        return self._config

    def create(self, comment: str, autogenerate: bool):
        command.revision(config=self.config, message=comment, autogenerate=autogenerate)

        if autogenerate:
            logrdata.logrobjc.warning(
                "Do not forget to edit the autogenerated migration script before executing it "
                + "or else any support relation not registered with the SQLAlchemy metadata will "
                + "be dropped."
            )

    def _get_current(self) -> Set[str]:
        scrtobjc = script.ScriptDirectory.from_config(self.config)

        curtrevs = set()

        def _get_rev_current(rev, context):
            curtrevs.update(
                _rev.cmd_format(verbose=False) for _rev in scrtobjc.get_all_current(rev)
            )
            return []

        with runtime.environment.EnvironmentContext(
            self.config, scrtobjc, fn=_get_rev_current(), dont_mutate=True
        ):
            scrtobjc.run_env()

        return curtrevs

    def db_version(self):
        logrdata.logrobjc.info("\n".join(self._get_current()))

    def upgrade(self, version: str):
        pre_revs = self._get_current()
        command.upgrade(self.config, version)
        post_revs = self._get_current()
        if pre_revs == post_revs:
            logrdata.logrobjc.warning("There is nothing to upgrade.")
        else:
            logrdata.logrobjc.info(f"Upgraded to {', '.join(post_revs)}")

    def downgrade(self, version: str):
        pre_revs = self._get_current()
        command.downgrade(self.config, version)
        post_revs = self._get_current()
        if pre_revs == post_revs:
            logrdata.logrobjc.warning("There is nothing to downgrade.")
        else:
            logrdata.logrobjc.info(
                f"Downgraded to {', '.join(post_revs) if post_revs else '<base>'}"
            )


alembic_migration = AlembicMigration()