import aiohttp
import json

from multidict import CIMultiDictProxy
from typing import Any


class HTTPBaseClientResponse:
    def __init__(self, status: int, headers: "CIMultiDictProxy[str]", body_data: bytearray):
        self.status = status
        self.headers = headers
        self.body_data = body_data

    def json(self) -> dict:
        try:
            if not self._json:
                self._json = json.loads(self.body_data.decode("utf-8"))
            return self._json
        except json.JSONDecodeError:
            raise Exception(f"Response is not a valid json format: {self.status} {self.text()}")

    def text(self) -> str:
        return self.body_data.decode("utf-8")


class HTTPBaseClient:
    @classmethod
    def create_session(cls, *args, **kwargs):
        cls.__session = aiohttp.ClientSession()

    @classmethod
    async def close_session(cls, *args, **kwargs):
        await cls.__session.close()

    def __init__(
        self,
        connect_timeout: float = None,
        socket_timeout: float = None,
        timeout: float = 5,
        backoff_sec: float = 1,
        retry: int = 0,
    ) -> None:
        self._connect_timeout = connect_timeout
        self._socket_timeout = socket_timeout
        self._timeout = timeout
        self._retry = retry
        self._backoff_sec = backoff_sec

    async def request(self, method: str, url: str, **kwargs: Any) -> HTTPBaseClientResponse:
        timeout = self._timeout
        error = None
        session = self.__session if hasattr(self, "_HTTPBaseClient__session") else aiohttp.ClientSession()

        for _ in range(self._retry + 1):
            try:
                async with session.request(
                    method=method,
                    url=url,
                    **kwargs,
                    timeout=aiohttp.ClientTimeout(
                        connect=self._connect_timeout,
                        sock_connect=self._socket_timeout,
                        total=timeout,
                    ),
                ) as response:
                    return HTTPBaseClientResponse(
                        status=response.status,
                        headers=response.headers,
                        body_data=await response.read(),
                    )
            except Exception as e:
                error = e
                timeout = timeout + self._backoff_sec

        raise error
