import click

from badges_server import __vers__, readconf
from badges_server.database.data.formatdb import make_database


@click.group(name="badges_server")
@click.option(
    "-c",
    "--conffile",
    "conffile",
    type=click.Path(exists=True),
    help="Read configuration from the specified Python file",
    default=None,
)
@click.version_option(version=__vers__, prog_name="badges_server")
def main(conffile=None):
    if conffile:
        confdict = {}
        with open(conffile) as confobjc:
            exec(compile(confobjc.read(), conffile, "exec"), confdict)
        readconf(confdict)


@main.command(name="setupdbs", help="Setup the database schema in the specified environment")
def setupdbs():
    make_database()
