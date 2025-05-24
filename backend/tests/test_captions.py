from io import BytesIO

import pytest
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from pixelgram.services.hf_client import get_hf_client
from pixelgram.settings import settings
from tests.overrides import override_fail_hf_client
from tests.utils import create_test_image


@pytest.fixture(autouse=True)
async def before_and_after():
    redis_connection = redis.from_url(
        settings.redis_uri, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


@pytest.mark.asyncio
async def test_generate_caption_valid():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        image = create_test_image()
        files = {"file": ("test.png", image, "image/png")}
        response = await ac.post("/captions/", files=files)

    assert response.status_code == 200
    assert response.json() == {"caption": "Mock caption"}


@pytest.mark.asyncio
async def test_generate_caption_invalid_size():
    image = create_test_image(size=(64, 64))
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("small.png", image, "image/png")}
        response = await ac.post("/captions/", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "Image must be 128x128 pixels."


@pytest.mark.asyncio
async def test_generate_caption_invalid_type():
    fake_file = BytesIO(b"Not an image")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("file.txt", fake_file, "text/plain")}
        response = await ac.post("/captions/", files=files)

    assert response.status_code == 400
    assert "Invalid content type" in response.json()["detail"]


@pytest.mark.asyncio
async def test_generate_caption_corrupt_image():
    corrupt_image = BytesIO(b"corruptdata")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("bad.png", corrupt_image, "image/png")}
        response = await ac.post("/captions/", files=files)

    assert response.status_code == 400
    assert "Invalid or corrupted image file." in response.json()["detail"]


@pytest.mark.asyncio
async def test_generate_caption_failure():
    app.dependency_overrides[get_hf_client] = override_fail_hf_client

    image = create_test_image()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("test.png", image, "image/png")}
        response = await ac.post("/captions/", files=files)

    assert response.status_code == 500
    assert "Failed to generate caption." in response.json()["detail"]

    app.dependency_overrides.pop(get_hf_client)


@pytest.mark.asyncio
async def test_generate_caption_too_many_requests():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        for _ in range(30):
            image = create_test_image()
            files = {"file": ("test.png", image, "image/png")}
            response = await ac.post("/captions/", files=files)

            if response.status_code == 429:
                break

    assert response.status_code == 429
    assert "Too Many Requests" in response.text
