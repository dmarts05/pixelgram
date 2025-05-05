from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from pixelgram.services.hf_client import get_hf_client
from tests.overrides import override_fail_hf_client
from tests.utils import create_test_image


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
