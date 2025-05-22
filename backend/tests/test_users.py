import pytest
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from tests.utils import create_test_post, create_test_user


@pytest.mark.asyncio
async def test_get_username_by_id_success():
    """Test successfully retrieving a user's info by ID."""
    user_id = "00000000-0000-0000-0000-000000000001"
    username = "testuser"

    async with app.router.lifespan_context(app):
        # Create a test user
        await create_test_user(id=user_id, username=username)

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.get(f"/users/{user_id}/info")

            assert response.status_code == 200
            user_data = response.json()
            assert user_data["id"] == user_id
            assert user_data["username"] == username


@pytest.mark.asyncio
async def test_get_username_by_id_not_found():
    """Test retrieving a non-existent user returns 404."""
    non_existent_id = "00000000-0000-0000-0000-000000000999"

    async with app.router.lifespan_context(app):
        # Create a test user to ensure we're authenticated
        await create_test_user()

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.get(f"/users/{non_existent_id}/info")

            assert response.status_code == 404
            assert response.json()["detail"] == "User not found."


@pytest.mark.asyncio
async def test_get_username_by_id_invalid_uuid():
    """Test that providing an invalid UUID format returns an error."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/users/not-a-uuid/info")

        assert response.status_code == 422  # Validation error

        @pytest.mark.asyncio
        async def test_delete_me_success():
            """Test successful deletion of the current user account and their posts."""
            user_id = "00000000-0000-0000-0000-000000000002"
            username = "deleteuser"

            async with app.router.lifespan_context(app):
                await create_test_user(id=user_id, username=username)

                async with AsyncClient(
                    transport=ASGITransport(app=app), base_url="http://test"
                ) as ac:
                    # Optionally, create posts for this user
                    post_id = await create_test_post(
                        user_id=user_id, content="Test post 1", client=ac
                    )
                    post_id2 = await create_test_post(
                        user_id=user_id, content="Test post 2", client=ac
                    )

                    # Simulate authentication (e.g., via cookie or header)
                    response = await ac.delete("/users/me")
                    assert response.status_code == 204

                    # Try to get the user info after deletion
                    response = await ac.get(f"/users/{user_id}/info")
                    assert response.status_code == 404

                    # Check that the user's posts have been deleted
                    response = await ac.get(f"/posts/{post_id}")
                    assert response.status_code == 404
                    response = await ac.get(f"/posts/{post_id2}")
                    assert response.status_code == 404

        @pytest.mark.asyncio
        async def test_delete_me_unauthorized():
            """Test deleting account without authentication returns 401."""
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                response = await ac.delete("/users/me")
                assert response.status_code == 401
