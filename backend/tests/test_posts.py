from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient
from PIL import Image

from pixelgram.__main__ import app
from pixelgram.auth import current_active_user
from pixelgram.models.user import User


def create_test_image(size=(128, 128), format="PNG", color="blue"):
    img = Image.new("RGB", size, color=color)
    buffer = BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer


async def override_current_user():
    return User(
        id="user-123", username="test_user", email="test@example.com", is_active=True
    )


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[current_active_user] = override_current_user
    yield
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_create_post_success(monkeypatch):
    class MockSupabaseClient:
        async def upload(self, image):
            return "https://mockstorage.com/image.png"

    monkeypatch.setattr(
        "pixelgram.routers.posts.SupabaseStorageClient", MockSupabaseClient
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        image = create_test_image()
        files = {"file": ("valid.png", image, "image/png")}
        data = {"description": "A valid post image"}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 201
    assert response.json()["post"]["description"] == "A valid post image"
    assert response.json()["post"]["image_url"] == "https://mockstorage.com/image.png"


@pytest.mark.asyncio
async def test_create_post_invalid_image_size():
    image = create_test_image(size=(64, 64))
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("small.png", image, "image/png")}
        data = {"description": "Too small image"}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 400
    assert "128x128 pixels" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_invalid_content_type():
    fake_file = BytesIO(b"This is not an image")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("file.txt", fake_file, "text/plain")}
        data = {"description": "Text file upload"}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 400
    assert "Invalid content type" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_corrupt_image():
    corrupt = BytesIO(b"notavalidimage")
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("corrupt.png", corrupt, "image/png")}
        data = {"description": "Broken image"}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 400
    assert "Invalid or corrupted image file" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_oversized_image(monkeypatch):
    class MockSettings:
        max_img_mb_size = 0.0001  # Simula 0.1KB límite para forzar fallo

    monkeypatch.setattr("pixelgram.routers.posts.settings", MockSettings)

    large_image = create_test_image()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("large.png", large_image, "image/png")}
        data = {"description": "Large image"}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 400
    assert "size limit" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_supabase_upload_failure(monkeypatch):
    class FailingSupabaseClient:
        async def upload(self, image):
            raise Exception("Supabase failed")

    monkeypatch.setattr(
        "pixelgram.routers.posts.SupabaseStorageClient", FailingSupabaseClient
    )

    image = create_test_image()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("fail.png", image, "image/png")}
        data = {"description": "Should fail upload"}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 500
    assert "Failed to save post" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_post_missing_description():
    image = create_test_image()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("missingdesc.png", image, "image/png")}
        response = await ac.post("/posts/", files=files)

    assert (
        response.status_code == 422
    )  # FastAPI validation error for missing form field
