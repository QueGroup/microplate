import asyncio
import logging
import time
from contextlib import contextmanager
from datetime import timedelta
from typing import Any, Callable, Generator

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from redis.asyncio import Redis
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from ..response import OkResponse
from ..urls import Paths

healthcheck_router = APIRouter()


@contextmanager
def measure_time() -> Generator[Callable[..., float]]:
    start_time = time.time()
    yield lambda: time.time() - start_time


async def check_db_health(session: AsyncSession) -> dict[str, Any]:
    stmt = select(text("1"))
    with measure_time() as get_time_taken:
        try:
            await asyncio.wait_for(session.execute(stmt), timeout=2.0)
            service_status = "Healthy"
        except Exception as ex:
            logging.error(f"Database health check failed: {ex}")
            service_status = "Unhealthy"
        time_taken = get_time_taken()

    return {
        "alias": "postgres db",
        "status": service_status,
        "timeTaken": time_taken,
    }


async def check_redis_health(r_client: Redis) -> dict[str, Any]:
    with measure_time() as get_time_taken:
        try:
            await asyncio.wait_for(r_client.ping(), timeout=2.0)
            service_status = "Healthy"
        except Exception as ex:
            logging.error(f"Redis health check failed: {ex}")
            service_status = "Unhealthy"
        time_taken = get_time_taken()

    return {
        "alias": "redis",
        "status": service_status,
        "timeTaken": time_taken,
    }


@healthcheck_router.get(
    path=Paths.HEALTHCHECK,
    response_model=OkResponse[dict[str, Any]],
    status_code=status.HTTP_200_OK,
    description="Healthcheck endpoint",
    summary="Healthcheck",
)
@inject
async def healthcheck_handler(
    session: FromDishka[AsyncSession],
    r_client: FromDishka[Redis],
) -> OkResponse[dict[str, Any]]:
    entities: list[dict[str, Any]] = []

    async with asyncio.TaskGroup() as tg:
        db_health_task = tg.create_task(check_db_health(session))
        redis_health_task = tg.create_task(check_redis_health(r_client))

    db_health = db_health_task.result()
    redis_health = redis_health_task.result()
    entities.extend([db_health, redis_health])

    total_time_taken_seconds = sum(entity["timeTaken"] for entity in entities)
    total_time_taken = timedelta(seconds=total_time_taken_seconds)

    for entity in entities:
        entity["timeTaken"] = str(timedelta(seconds=entity["timeTaken"]))

    return OkResponse(
        status=200,
        result={
            "status": (
                "Healthy"
                if all(entity["status"] == "Healthy" for entity in entities)
                else "Unhealthy"
            ),
            "totalTimeTaken": str(total_time_taken),
            "entities": entities,
        },
    )
