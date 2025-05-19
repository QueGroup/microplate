import logging
from functools import partial
from typing import Awaitable, Callable

from domain.common import AppError
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from presentation.api.v1.response import ErrorData, ErrorResponse

logger = logging.getLogger(__name__)

ex_mappers = {
    AppError: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def setup_exception_handlers(app: FastAPI) -> None:
    for exception, status_code in ex_mappers.items():
        app.add_exception_handler(exception, error_handler(status_code))
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(
    status_code: int,
) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: AppError, status_code: int
) -> ORJSONResponse:
    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(title=err.title, data=err),
        status_code=status_code,
        status_=ex_mappers[type(err)],
    )


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=ErrorData(data=err)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,  # type: ignore
    status_code: int,
    status_: int,
) -> ORJSONResponse:
    if status_code == 500 or status_ == 500:
        logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status_),
        status_code=status_code,
    )
