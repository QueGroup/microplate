import abc
import logging
from typing import Annotated, Any, Literal, Mapping

import backoff
import httpx
from pydantic import BaseModel, Field


class Response(BaseModel):
    status_code: int
    data: Annotated[list[dict[str, Any]] | dict[str, Any], Field(...)] = Field(
        default={}
    )


class BaseClient(abc.ABC):

    def __init__(self, url: str, timeout: int = 20) -> None:
        self._url = url
        self._timeout = timeout
        self.log = logging.getLogger(self.__class__.__name__)

    @backoff.on_exception(
        backoff.expo,
        (httpx.ConnectError, httpx.RequestError),
        max_time=20,
    )
    async def _make_request(
        self,
        path: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        data: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
    ) -> Response:
        """
        Make an HTTP request
        :param path: API endpoint path
        :param method: HTTP method
        :param params: Query parameters for the request
        :param headers: Headers for the request
        :param data: Data for the request
        :param json: JSON data for the request
        :return: The response from the API
        """
        request_url = f"{self._url}{path}"
        if headers is None:
            headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient(
            base_url=self._url,
            headers=headers,
            timeout=self._timeout,
        ) as client:
            self.log.debug(
                "Making request %r %r with json %r and params %r",
                method,
                request_url,
                json,
                params,
            )
            try:
                response = await client.request(
                    method=method,
                    params=params,
                    json=json,
                    data=data,
                    headers=headers,
                    url=request_url,
                )
                response.raise_for_status()
                return Response(data=response.json(), status_code=response.status_code)
            except httpx.HTTPStatusError as e:
                self.log.error(
                    "Request to %r %r failed with status code %r and error %r",
                    method,
                    request_url,
                    e.response.status_code,
                    e.response.text,
                )
                return Response(status_code=e.response.status_code)
            except httpx.RequestError as e:
                self.log.error(
                    "Request to %r %r failed with error %r",
                    method,
                    request_url,
                    str(e),
                )
                return Response(status_code=500, data={"error": str(e)})

    async def get(
        self,
        path: str,
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        return await self._make_request(
            path, method="GET", params=params, headers=headers
        )

    async def post(
        self,
        path: str,
        json: Mapping[str, str] | None = None,
        data: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        return await self._make_request(
            path, method="POST", json=json, data=data, headers=headers
        )

    async def patch(
        self,
        path: str,
        json: Mapping[str, str] | None = None,
        data: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        return await self._make_request(
            path, method="PATCH", json=json, data=data, headers=headers
        )

    async def delete(
        self,
        path: str,
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        return await self._make_request(path, "DELETE", params=params, headers=headers)
