from pytest import mark
from tests.client import redis


@mark.asyncio
async def test_ping() -> None:
    async with redis:
        assert await redis.ping() == "PONG"


@mark.asyncio
async def test_ping_with_message() -> None:
    async with redis:
        assert await redis.ping(message="Upstash is nice!") == "Upstash is nice!"