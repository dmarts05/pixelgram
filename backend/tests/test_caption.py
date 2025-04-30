from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient
from PIL import Image

from pixelgram.__main__ import app
from pixelgram.auth import current_active_user
from pixelgram.models.user import User


def create_test_image(size=(128, 128), format="PNG"):
    img = Image.new("RGB", size, color="red")
    buffer = BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer


async def override_current_user():
    return User(
        id="123", username="test_user", email="test@example.com", is_active=True
    )


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[current_active_user] = override_current_user
    yield
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_generate_caption_valid(monkeypatch):
    # Define una clase mock para HFClient
    class MockHFClient:
        async def generate_caption(self, img_bytes):
            return "Mock caption"

    monkeypatch.setattr("pixelgram.routers.captions.HFClient", MockHFClient)

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
async def test_generate_caption_failure(monkeypatch):
    class MockHFClient:
        async def generate_caption(self, img_bytes):
            return None

    monkeypatch.setattr("pixelgram.routers.captions.HFClient", MockHFClient)

    image = create_test_image()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("test.png", image, "image/png")}
        response = await ac.post("/captions/", files=files)

    assert response.status_code == 500
    assert "Failed to generate caption." in response.json()["detail"]
