import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.database import Base, DATABASE_URL  # import your Base and DB URL
import app.models  # make sure models are imported so Alembic sees them

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(connection=conn, target_metadata=target_metadata)
        )

        await connection.run_sync(lambda conn: context.begin_transaction())
        await connection.run_sync(lambda conn: context.run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
