from typing import AsyncIterable

import backoff
from dishka import Provider, Scope, provide
from environs import Env
from infra.config import Config, DbConfig, RedisConfig
from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self) -> Config:
        env = Env()
        env.read_env()

        return Config(
            db=DbConfig.from_env(env),
            redis=RedisConfig.from_env(env),
        )

    @provide(scope=Scope.APP)
    def provide_db(self, config: Config) -> DbConfig:
        return config.db

    @provide(scope=Scope.APP)
    def provide_redis(self, config: Config) -> RedisConfig:
        return config.redis


class SqlalchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self, config: DbConfig) -> AsyncEngine:
        return create_async_engine(
            config.construct_sqlalchemy_url,
            pool_size=10,
            max_overflow=5,
        )

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()
            finally:
                await session.close()


class RedisProvider(Provider):
    scope = Scope.APP

    @backoff.on_exception(
        backoff.expo,
        ConnectionError,
        max_tries=5,
        giveup=lambda e: e.args[0] != "Connection Error",
    )
    @provide(scope=Scope.REQUEST)
    async def provide_redis(self, config: RedisConfig) -> AsyncIterable[Redis]:
        async with Redis.from_url(
            config.construct_redis_dsn, decode_responses=True
        ) as r_client:
            yield r_client


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST
