import pytest
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from pixelgram.auth import current_active_user  # noqa: E402
from tests.utils import (
    create_test_image,
    create_test_user,
    get_test_user,
)


@pytest.mark.asyncio
async def test_post_comment_success():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("comment.png", image, "image/png")}
            data = {"description": "Comment test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            comment_data = {"content": "This is a test comment"}
            comment_resp = await ac.post(
                f"/posts/{post_id}/comments/", json=comment_data
            )
            assert comment_resp.status_code == 201
            assert "comment" in comment_resp.json()
            assert "id" in comment_resp.json()["comment"]
            assert comment_resp.json()["comment"]["content"] == "This is a test comment"


@pytest.mark.asyncio
async def test_post_comment_missing_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        comment_data = {"content": "This is a test comment"}
        comment_resp = await ac.post(
            "/posts/00000000-0000-0000-0000-000000000001/comments/", json=comment_data
        )
        assert comment_resp.status_code == 404
        assert comment_resp.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_post_comment_invalid_content():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("comment_invalid.png", image, "image/png")}
            data = {"description": "Comment test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            comment_data = {"content": ""}
            comment_resp = await ac.post(
                f"/posts/{post_id}/comments/", json=comment_data
            )
            assert comment_resp.status_code == 422


@pytest.mark.asyncio
async def test_post_comment_content_too_long():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("comment_long.png", image, "image/png")}
            data = {"description": "Comment test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            long_comment = "A" * 1001
            comment_data = {"content": long_comment}
            comment_resp = await ac.post(
                f"/posts/{post_id}/comments/", json=comment_data
            )
            assert comment_resp.status_code == 422


@pytest.mark.asyncio
async def test_get_comments_success():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("get_comments.png", image, "image/png")}
            data = {"description": "Get comments test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            comment_data = {"content": "This is a test comment"}
            await ac.post(f"/posts/{post_id}/comments/", json=comment_data)

            get_comments_resp = await ac.get(f"/posts/{post_id}/comments/")
            assert get_comments_resp.status_code == 200
            json = get_comments_resp.json()
            assert "data" in json
            assert len(json["data"]) == 1
            assert json["data"][0]["content"] == "This is a test comment"
            assert "nextPage" in json
            assert json["nextPage"] is None
            assert "total" in json
            assert json["total"] == 1


@pytest.mark.asyncio
async def test_get_comments_empty():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("empty_comments.png", image, "image/png")}
            data = {"description": "Empty comments test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            get_comments_resp = await ac.get(f"/posts/{post_id}/comments/")
            assert get_comments_resp.status_code == 200
            json = get_comments_resp.json()
            assert "data" in json
            assert len(json["data"]) == 0
            assert "nextPage" in json
            assert json["nextPage"] is None
            assert "total" in json
            assert json["total"] == 0


@pytest.mark.asyncio
async def test_get_comments_pagination():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("pagination_comments.png", image, "image/png")}
            data = {"description": "Pagination comments test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            # Create 15 comments
            for i in range(15):
                comment_data = {"content": f"Comment {i + 1}"}
                await ac.post(f"/posts/{post_id}/comments/", json=comment_data)

            get_comments_resp = await ac.get(
                f"/posts/{post_id}/comments/", params={"page": 1, "page_size": 10}
            )
            assert get_comments_resp.status_code == 200
            json = get_comments_resp.json()
            assert "data" in json
            assert len(json["data"]) == 10
            assert "nextPage" in json
            assert json["nextPage"] == 2
            assert "total" in json
            assert json["total"] == 15

            # Get second page
            get_comments_resp = await ac.get(
                f"/posts/{post_id}/comments/", params={"page": 2, "page_size": 10}
            )
            assert get_comments_resp.status_code == 200
            json = get_comments_resp.json()
            assert "data" in json
            assert len(json["data"]) == 5
            assert "nextPage" in json
            assert json["nextPage"] is None
            assert "total" in json
            assert json["total"] == 15


@pytest.mark.asyncio
async def test_get_comments_invalid_page():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("invalid_page.png", image, "image/png")}
            data = {"description": "Invalid page test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            get_comments_resp = await ac.get(
                f"/posts/{post_id}/comments/", params={"page": 0, "page_size": 10}
            )
    assert get_comments_resp.status_code == 422


@pytest.mark.asyncio
async def test_get_comments_invalid_query_params():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("invalid_query.png", image, "image/png")}
            data = {"description": "Invalid query test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            get_comments_resp = await ac.get(
                f"/posts/{post_id}/comments/",
                params={"page": "invalid", "page_size": "invalid"},
            )
    assert get_comments_resp.status_code == 422


@pytest.mark.asyncio
async def test_get_comments_no_query_params():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("no_query.png", image, "image/png")}
            data = {"description": "No query params test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            get_comments_resp = await ac.get(f"/posts/{post_id}/comments/")
    assert get_comments_resp.status_code == 200
    json = get_comments_resp.json()
    assert "data" in json
    assert len(json["data"]) == 0
    assert "nextPage" in json
    assert json["nextPage"] is None
    assert "total" in json
    assert json["total"] == 0


@pytest.mark.asyncio
async def test_get_comments_page_number_out_of_range():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("out_of_range.png", image, "image/png")}
            data = {"description": "Out of range test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            get_comments_resp = await ac.get(
                f"/posts/{post_id}/comments/", params={"page": 2, "page_size": 3}
            )
    assert get_comments_resp.status_code == 200
    json = get_comments_resp.json()
    assert "data" in json
    assert len(json["data"]) == 0
    assert "nextPage" in json
    assert json["nextPage"] is None
    assert "total" in json
    assert json["total"] == 0


@pytest.mark.asyncio
async def test_delete_comment_success():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("delete_comment.png", image, "image/png")}
            data = {"description": "Delete comment test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            comment_data = {"content": "This is a test comment"}
            comment_resp = await ac.post(
                f"/posts/{post_id}/comments/", json=comment_data
            )
            comment_id = comment_resp.json()["comment"]["id"]

            delete_resp = await ac.delete(f"/posts/{post_id}/comments/{comment_id}/")
            assert delete_resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_comment_missing_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        delete_resp = await ac.delete(
            "/posts/00000000-0000-0000-0000-000000000001/comments/00000000-0000-0000-0000-000000000002/"
        )
    assert delete_resp.status_code == 404
    assert delete_resp.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_delete_comment_missing_comment():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("missing_comment.png", image, "image/png")}
            data = {"description": "Missing comment test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            delete_resp = await ac.delete(
                f"/posts/{post_id}/comments/00000000-0000-0000-0000-000000000002/"
            )
    assert delete_resp.status_code == 404
    assert delete_resp.json()["detail"] == "Comment not found"


@pytest.mark.asyncio
async def test_delete_comment_not_authorized():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("not_authorized.png", image, "image/png")}
            data = {"description": "Not authorized test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            comment_data = {"content": "This is a test comment"}
            comment_resp = await ac.post(
                f"/posts/{post_id}/comments/", json=comment_data
            )
            comment_id = comment_resp.json()["comment"]["id"]

            # Simulate a different user trying to delete the comment
            app.dependency_overrides[current_active_user] = lambda: get_test_user(
                id="00000000-0000-0000-0000-000000000003",
                username="unauthorized_user",
                email="unauthorized_user@example.com",
            )

            delete_resp = await ac.delete(f"/posts/{post_id}/comments/{comment_id}/")
            assert delete_resp.status_code == 403
