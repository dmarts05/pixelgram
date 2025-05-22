import pytest
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from tests.utils import (
    create_test_user,
    create_test_post,
)


@pytest.mark.asyncio
async def test_save_post_and_verify():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="Test save post", client=ac)

            save_resp = await ac.post(f"/posts/{post_id}/save/")
            assert save_resp.status_code == 204

            get_resp = await ac.get("/posts/saved/")
            assert get_resp.status_code == 200
            post = next(p for p in get_resp.json()["data"] if p["id"] == post_id)
            assert post["savedByUser"] is True
            assert get_resp.json()["total"] == 1


@pytest.mark.asyncio
async def test_save_post_already_saved():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="Already saved post", client=ac)

            first_save_resp = await ac.post(f"/posts/{post_id}/save/")
            assert first_save_resp.status_code == 204

            second_save_resp = await ac.post(f"/posts/{post_id}/save/")
            assert second_save_resp.status_code == 409


@pytest.mark.asyncio
async def test_save_post_missing_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.post("/posts/00000000-0000-0000-0000-000000000001/save/")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_unsave_post_and_verify():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="Test unsave post", client=ac)
            await ac.post(f"/posts/{post_id}/save/")

            unsave_resp = await ac.delete(f"/posts/{post_id}/save/")
            assert unsave_resp.status_code == 204

            get_resp = await ac.get("/posts/saved/")
            assert get_resp.status_code == 200
            assert get_resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_unsave_post_not_saved():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="Not saved post", client=ac)

            unsave_resp = await ac.delete(f"/posts/{post_id}/save/")
            assert unsave_resp.status_code == 400


async def test_unsave_post_missing_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.delete("/posts/00000000-0000-0000-0000-000000000001/save/")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Post not found"
