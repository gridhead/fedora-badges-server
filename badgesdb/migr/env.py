from alembic import context
from sqlalchemy import engine_from_config, pool

from badgesdb.data import metadata

confobjc = context.config

destmeta = metadata


def run_migrations_offline():
    """
    Run migrations in OFFLINE mode

    This configures the context with just a database location and not a
    database engine object, though a database engine object is acceptable here
    as well. By skipping the process of creating the database engine object -
    we do not even need a database API to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    baselink = confobjc.get_main_option("sqlalchemy.url")
    context.configure(
        url=baselink,
        target_metadata=destmeta,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in ONLINE mode

    A database engine object is required to associate a connection with the
    context.
    """
    connable = engine_from_config(
        confobjc.get_section(confobjc.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connable.connect() as connobjc:
        context.configure(connection=connobjc, target_metadata=destmeta)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
