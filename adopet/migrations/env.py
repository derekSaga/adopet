import asyncio
import os
import sys

from alembic import context
from alembic import operations
from sqlalchemy import inspect
from sqlalchemy import pool
from sqlalchemy import schema
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config


def process_revision_directives(context, revision, directives):
    """Modify the MigrationScript directives to create schemata as required."""
    script = directives[0]
    tables_list = [table for tg in target_metadata for table in tg.tables.values()]
    for schema in frozenset(i.schema for i in tables_list):
        script.upgrade_ops.ops.insert(
            0, operations.ops.ExecuteSQLOp(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        )
        script.downgrade_ops.ops.append(
            operations.ops.ExecuteSQLOp(f"DROP SCHEMA IF EXISTS {schema} RESTRICT")
        )


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
sys.path.append(BASE_DIR)

from adopet.api.models import animal_specie_model
from adopet.api.models import city_model
from adopet.api.models import pet_model
from adopet.api.models import size_model
from adopet.api.models import state_model
from adopet.api.models import status_model
from adopet.api.models import user_model
from adopet.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import my_model
# target_metadata = my_model.Base.metadata

url_connection = "postgresql+asyncpg://%s:%s@%s/%s" % (
    os.environ["POSTGRES_USER"],
    os.environ["POSTGRES_PASSWORD"],
    f"{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}",
    os.environ["POSTGRES_DB"],
)

config.set_main_option("sqlalchemy.url", url_connection)

target_metadata = [
    state_model.StateModel.metadata,
    city_model.CityModel.metadata,
    animal_specie_model.AnimalSpecieModel.metadata,
    size_model.SizeModel.metadata,
    status_model.StatusModel.metadata,
    user_model.UserModel.metadata,
    pet_model.PetModel.metadata,
]


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True,
        version_table_schema=settings.DATABASE_SCHEMA,
        process_revision_directives=process_revision_directives,
    )
    context.execute(f"create schema if not exists {settings.DATABASE_SCHEMA};")

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
