# Comando para alembic
# uv run alembic revision --autogenerate -m "nombre del commit"

# Para SQLITE
# $env:DB_ENGINE="sqlite"; uv run alembic revision --autogenerate -m ""
# $env:DB_ENGINE="sqlite"; uv run alembic upgrade head

# Para POSTGRES
# $env:DB_ENGINE="postgres"; uv run alembic revision --autogenerate -m ""
# $env:DB_ENGINE="postgres"; uv run alembic upgrade head

# uv run alembic upgrade head
# uv run alembic downgrade -1
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Asegúrate de importar también el path de SQLite
from config.constants_common import DB_PATH_POSTGRES, DB_PATH_SQLITE

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from infrastructure import dbbase_postgres
from infrastructure import dbbase_sqlite
import infrastructure.db.models
from infrastructure.db.models.gomeria.movimientos_model import GomeriaMovimientosModel

config = context.config

db_engine = os.environ.get("DB_ENGINE", "postgres")

if db_engine == "sqlite":
    config.set_main_option("sqlalchemy.url", DB_PATH_SQLITE)
    target_metadata = dbbase_sqlite.metadata
else:
    config.set_main_option("sqlalchemy.url", DB_PATH_POSTGRES)
    target_metadata = dbbase_postgres.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Configuramos los parámetros base
        context_kwargs = {
            "connection": connection,
            "target_metadata": target_metadata,
            "compare_type": True,
            "render_as_batch": True,
        }

        if db_engine == "postgres":
            context_kwargs["version_table_schema"] = 'estadisticas'
            context_kwargs["include_schemas"] = True

        context.configure(**context_kwargs)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()