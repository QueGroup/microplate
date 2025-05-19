import logging
import os
from typing import AsyncGenerator, Generator

import orjson
import pytest
import pytest_asyncio
from alembic.config import Config as AlembicConfig
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from httpx import ASGITransport, AsyncClient
from infra import ConfigProvider, InteractorProvider, RepositoriesProvider
from infra.db import Base
from main import create_app
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from tests.mocks import MockSqlalchemyProvider

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:15-alpine")
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        logger.info("postgres url %s", postgres_url_)
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(autouse=True, scope="session")
def app():
    yield create_app()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig()
    script_location = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "src",
        "infrastructure",
        "db",
        "migrations",
    )
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    logger.info("Alembic config: %s", alembic_cfg.get_main_option("sqlalchemy.url"))
    return alembic_cfg


@pytest.fixture(autouse=True, scope="session")
async def setup_db(postgres_url: str) -> None:
    engine = create_async_engine(
        url=postgres_url,
        json_serializer=lambda o: orjson.dumps(o).decode(),
        json_deserializer=orjson.loads,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session_factory(
        postgres_url: str,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    engine = create_async_engine(
        url=postgres_url,
        json_serializer=lambda o: orjson.dumps(o).decode(),
        json_deserializer=orjson.loads,
    )
    session_factory_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    yield session_factory_
    await engine.dispose()


@pytest_asyncio.fixture
async def session(
        session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session_:
        yield session_


@pytest.fixture(scope="session")
def container(postgres_url: str):
    container = make_async_container(
        MockSqlalchemyProvider(postgres_url),
        ConfigProvider(),
        RepositoriesProvider(),
        InteractorProvider(),
    )
    yield container


@pytest_asyncio.fixture(scope="session")
async def ac(app, container):
    setup_dishka(container, app)
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
