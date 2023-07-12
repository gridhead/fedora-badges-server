import os

import click

from badges_server import __vers__, readconf
from badges_server.database.data.formatdb import make_database
from badges_server.system.main import start_service


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
        os.environ["FSBS_CONFFILE"] = os.path.abspath(conffile)
        readconf()


@main.command(name="setup", help="Setup the database schema in the specified environment")
def setup():
    make_database()


@main.command(name="serve", help="Start the Badges Server application")
def serve():
    start_service()
