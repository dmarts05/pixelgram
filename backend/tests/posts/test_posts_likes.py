import pytest
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from tests.utils import (
    create_test_user,
    create_test_post,
)


@pytest.mark.asyncio
async def test_like_and_verify():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="Test post", client=ac)

            like_resp = await ac.post(f"/posts/{post_id}/like/")
            assert like_resp.status_code == 204

            get_resp = await ac.get("/posts/")
            post = next(p for p in get_resp.json()["data"] if p["id"] == post_id)
            assert post["likesCount"] == 1
            assert post["likedByUser"] is True


@pytest.mark.asyncio
async def test_duplicate_like():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="Dup", client=ac)

            first = await ac.post(f"/posts/{post_id}/like/")
            assert first.status_code == 204
            second = await ac.post(f"/posts/{post_id}/like/")
            assert second.status_code == 409
            assert "already liked" in second.json()["detail"].lower()


@pytest.mark.asyncio
async def test_like_missing_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.post("/posts/00000000-0000-0000-0000-000000000001/like/")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_unlike_and_verify():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="Unlike", client=ac)
            await ac.post(f"/posts/{post_id}/like/")

            await ac.delete(f"/posts/{post_id}/like/")

            get_resp = await ac.get("/posts/")
            post = next(p for p in get_resp.json()["data"] if p["id"] == post_id)
            assert post["likesCount"] == 0
            assert post["likedByUser"] is False


@pytest.mark.asyncio
async def test_unlike_without_like():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_id = await create_test_post(content="No like", client=ac)

            del_resp = await ac.delete(f"/posts/{post_id}/like/")
            assert del_resp.status_code == 400
            assert "not liked" in del_resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_unlike_missing_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.delete("/posts/00000000-0000-0000-0000-000000000001/like/")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Post not found"
