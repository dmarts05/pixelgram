from datetime import datetime
from io import BytesIO
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from tests.utils import create_test_image, override_current_user

id = uuid4()
created_at = datetime.now()


@pytest.fixture(autouse=True)
def override_dependencies():
    class MockAsyncSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args, **kwargs):
            pass

        async def commit(self):
            pass

        def add(self, obj):
            pass

        async def refresh(self, obj):
            obj.id = id
            obj.created_at = created_at
            return obj

        async def rollback(self):
            pass

    async def mock_get_async_session():
        return MockAsyncSession()

    # Set up overrides
    app.dependency_overrides[current_active_user] = override_current_user
    app.dependency_overrides[get_async_session] = mock_get_async_session

    yield

    # Clean up overrides
    app.dependency_overrides = {}


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
        max_img_mb_size = 0.0001  # Simulate a very small size limit

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


@pytest.mark.asyncio
async def test_create_post_success(monkeypatch):
    # Mock Supabase client for getting a predictable URL without actual upload
    mock_image_url = "https://example.com/test-image.png"

    class SuccessSupabaseClient:
        def __init__(self, *args, **kwargs):
            pass

        async def upload(self, *args, **kwargs):
            return mock_image_url

    monkeypatch.setattr(
        "pixelgram.routers.posts.SupabaseStorageClient", SuccessSupabaseClient
    )

    # Create a valid image and description
    image = create_test_image()
    test_description = "Test successful post"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("success.png", image, "image/png")}
        data = {"description": test_description}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 200
    resp_data = response.json()

    # Verify structure and content
    assert "post" in resp_data
    assert resp_data["post"]["description"] == test_description
    assert resp_data["post"]["image_url"] == mock_image_url
    assert "id" in resp_data["post"]
    assert resp_data["post"]["id"] == str(id)
    assert "created_at" in resp_data["post"]
    assert resp_data["post"]["created_at"] == created_at.isoformat()
