import pytest
from fastapi import APIRouter, Request
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from pixelgram.limiter import limiter


@pytest.fixture
def mount_rate_limit_test_route():
    rate_limit_router = APIRouter()

    @rate_limit_router.get("/rate-limit-test")
    @limiter.limit("3/minute")
    async def rate_limited_route(request: Request):
        return {"message": "Success"}

    app.include_router(rate_limit_router)

    yield

    app.router.routes = [
        route
        for route in app.router.routes
        if getattr(route, "path", None) != "/rate-limit-test"
    ]


@pytest.mark.asyncio
async def test_rate_limiter_blocks_after_limit(mount_rate_limit_test_route):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Send 3 requests within the limit
        for _ in range(3):
            response = await ac.get("/rate-limit-test")
            assert response.status_code == 200

        # This request should exceed the limit
        response = await ac.get("/rate-limit-test")
        assert response.status_code == 429
        assert "rate limit exceeded" in response.text.lower()
