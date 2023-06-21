import click

from badgesdb import __vers__, readconf
from badgesdb.data.formatdb import make_database


@click.group(name="badgesdb")
@click.option(
    "-c",
    "--conffile",
    "conffile",
    type=click.Path(exists=True),
    help="Read configuration from the specified Python file",
    default=None,
)
@click.version_option(version=__vers__, prog_name="badgesdb")
def main(conffile=None):
    if conffile:
        confdict = {}
        with open(conffile) as confobjc:
            exec(compile(confobjc.read(), conffile, "exec"), confdict)
        readconf(confdict)


@main.command(name="setupdbs", help="Setup the database schema in the specified environment")
def setupdbs():
    make_database()
