"""Synthetic asynchronous HTTP responses for network-isolated adapter tests."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import httpx

from .adapter import HttpSnapshotAdapter


@dataclass(frozen=True, slots=True)
class SyntheticResponse:
    status_code: int = 200
    headers: tuple[tuple[str, str], ...] = (("content-type", "image/png"),)
    body: bytes = b""
    chunk_size: int = 8192
    delay_before_body: float = 0.0


class _SyntheticStream(httpx.AsyncByteStream):
    def __init__(self, body: bytes, chunk_size: int, delay_before_body: float):
        self._body = body
        self._chunk_size = max(1, chunk_size)
        self._delay_before_body = delay_before_body
        self.closed = False

    async def __aiter__(self):
        if self._delay_before_body:
            import asyncio

            await asyncio.sleep(self._delay_before_body)
        for offset in range(0, len(self._body), self._chunk_size):
            yield self._body[offset : offset + self._chunk_size]

    async def aclose(self) -> None:
        self.closed = True


class _SyntheticTransport(httpx.AsyncBaseTransport):
    def __init__(self, responder):
        self._responder = responder

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        return await self._responder(request)

    async def aclose(self) -> None:
        return None


class FakeHttpSnapshotAdapter(HttpSnapshotAdapter):
    """Production adapter backed only by queued in-memory HTTP responses."""

    def __init__(self, responses: list[SyntheticResponse]):
        self.requests: list[httpx.Request] = []
        self.streams: list[_SyntheticStream] = []
        self._responses = deque(responses)

        async def respond(request: httpx.Request) -> httpx.Response:
            self.requests.append(request)
            if not self._responses:
                raise AssertionError("Unexpected HTTP request in fake transport")
            fixture = self._responses.popleft()
            stream = _SyntheticStream(fixture.body, fixture.chunk_size, fixture.delay_before_body)
            self.streams.append(stream)
            return httpx.Response(
                fixture.status_code,
                headers=dict(fixture.headers),
                stream=stream,
                request=request,
            )

        super().__init__(transport=_SyntheticTransport(respond))
