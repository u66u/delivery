from litestar.plugins.sqlalchemy import (
    AlembicAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,

)
from litestar.utils.module_loader import module_to_os_path
from advanced_alchemy.base import metadata_registry

from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
import os

load_dotenv()

root_dir = module_to_os_path("app")

@dataclass
class DBConfig:
    name: str = os.getenv("DB_NAME", "postgres")
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "postgres")
    port: int = os.getenv("DB_PORT", 5432)
    host: str = os.getenv("DB_HOST", "localhost")
    url: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

    @property
    def engine(self) -> AsyncEngine:
        return create_async_engine(
            self.url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30.0,
            pool_recycle=600,
        )
    
    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(self.engine, expire_on_commit=False)

@dataclass
class BotConfig:
    token: str = os.getenv("BOT_TOKEN")

db_config = DBConfig()
alchemy = SQLAlchemyAsyncConfig(
    engine_instance=db_config.engine,
    before_send_handler="autocommit",
    metadata=metadata_registry.get(),
    session_config=AsyncSessionConfig(expire_on_commit=False),
    alembic_config=AlembicAsyncConfig(
        version_table_name="alembic_version",
        script_config=f"{root_dir}/db/alembic.ini",
        script_location=f"{root_dir}/db/migrations",
    ),
)