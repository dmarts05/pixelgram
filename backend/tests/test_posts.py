from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient

from pixelgram.__main__ import app
from pixelgram.auth import current_active_user  # noqa: E402
from pixelgram.settings import get_settings
from tests.overrides import override_small_image_size_settings
from tests.utils import (
    create_test_image,
    create_test_user,
    get_test_user,
)


@pytest.mark.asyncio
async def test_create_post_success():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("valid.png", image, "image/png")}
            data = {"description": "A valid post image"}
            response = await ac.post("/posts/", files=files, data=data)
            json_data = response.json()
            assert "post" in json_data
            assert "id" in json_data["post"]
            post_id = json_data["post"]["id"]
            assert post_id is not None
            assert json_data["post"]["description"] == "A valid post image"
            assert json_data["post"]["imageUrl"] is not None
            assert json_data["post"]["userId"] is not None
            assert json_data["post"]["authorUsername"] is not None
            assert json_data["post"]["authorEmail"] is not None
            assert json_data["post"]["createdAt"] is not None
            assert json_data["post"]["likesCount"] == 0
            assert json_data["post"]["likedByUser"] is False
            assert json_data["post"]["commentsCount"] == 0
            assert json_data["post"]["commentedByUser"] is False

    assert response.status_code == 201


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
async def test_create_post_oversized_image():
    app.dependency_overrides[get_settings] = override_small_image_size_settings

    large_image = create_test_image()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("large.png", large_image, "image/png")}
        data = {"description": "Large image"}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 400
    assert "size limit" in response.json()["detail"]

    app.dependency_overrides.pop(get_settings)


@pytest.mark.asyncio
async def test_create_post_missing_description():
    image = create_test_image()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("missingdesc.png", image, "image/png")}
        response = await ac.post("/posts/", files=files)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_post_description_too_long():
    image = create_test_image()
    long_description = "A" * 1001
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        files = {"file": ("longdesc.png", image, "image/png")}
        data = {"description": long_description}
        response = await ac.post("/posts/", files=files, data=data)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_posts_pagination():
    async with app.router.lifespan_context(app):
        await create_test_user()

        # Create a number of posts using the POST endpoint.
        num_posts = 15
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            for i in range(num_posts):
                image = create_test_image()
                files = {"file": ("valid.png", image, "image/png")}
                data = {"description": f"Post number {i + 1}"}
                resp = await ac.post("/posts/", files=files, data=data)
                # Assert that each post was created successfully.
                assert resp.status_code == 201, (
                    f"Post creation failed on iteration {i + 1}"
                )

            # Query page 1 with page_size 10.
            get_resp = await ac.get("/posts/", params={"page": 1, "page_size": 10})
            assert get_resp.status_code == 200, "GET posts failed for page 1"
            json_data = get_resp.json()
            # Expect 10 posts on the first page.
            assert "data" in json_data
            assert len(json_data["data"]) == 10
            # nextPage should be 2 since there are 15 posts.
            assert json_data["nextPage"] == 2
            assert json_data["total"] == num_posts

            # Query page 2 with the same page_size.
            get_resp = await ac.get("/posts/", params={"page": 2, "page_size": 10})
            assert get_resp.status_code == 200, "GET posts failed for page 2"
            json_data = get_resp.json()
            # Expect 5 posts on the second page.
            assert len(json_data["data"]) == 5
            # No further page available.
            assert json_data["nextPage"] is None
            assert json_data["total"] == num_posts


@pytest.mark.asyncio
async def test_get_posts_empty_database():
    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            get_resp = await ac.get("/posts/", params={"page": 1, "page_size": 10})
    assert get_resp.status_code == 200
    json_data = get_resp.json()
    assert json_data["data"] == []
    assert json_data["nextPage"] is None
    assert json_data["total"] == 0


@pytest.mark.asyncio
async def test_get_posts_minimum_page_size():
    async with app.router.lifespan_context(app):
        await create_test_user()
        # Create 5 posts.
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            for i in range(5):
                image = create_test_image()
                files = {"file": ("minpage.png", image, "image/png")}
                data = {"description": f"Minimum size post {i + 1}"}
                resp = await ac.post("/posts/", files=files, data=data)
                assert resp.status_code == 201

            # Request using page_size 1.
            get_resp = await ac.get("/posts/", params={"page": 1, "page_size": 1})
            assert get_resp.status_code == 200
            json_data = get_resp.json()
            assert len(json_data["data"]) == 1
            # As there are 5 posts, nextPage should be 2.
            assert json_data["nextPage"] == 2


@pytest.mark.asyncio
async def test_get_posts_maximum_page_size():
    async with app.router.lifespan_context(app):
        await create_test_user()
        # Create 20 posts.
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            for i in range(20):
                image = create_test_image()
                files = {"file": ("maxpage.png", image, "image/png")}
                data = {"description": f"Maximum size post {i + 1}"}
                resp = await ac.post("/posts/", files=files, data=data)
                assert resp.status_code == 201

            # Request using page_size 100.
            get_resp = await ac.get("/posts/", params={"page": 1, "page_size": 100})
            assert get_resp.status_code == 200
            json_data = get_resp.json()
            # Even though page_size is 100, only 20 posts exist.
            assert len(json_data["data"]) == 20
            assert json_data["nextPage"] is None
            assert json_data["total"] == 20


@pytest.mark.asyncio
async def test_get_posts_ordering():
    async with app.router.lifespan_context(app):
        # Create test user if necessary.
        await create_test_user()

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            # Create two posts in sequence.
            image = create_test_image()
            files = {"file": ("first.png", image, "image/png")}
            data = {"description": "First Post"}
            resp1 = await ac.post("/posts/", files=files, data=data)
            assert resp1.status_code == 201

            # Create a second post.
            image = create_test_image()
            files = {"file": ("second.png", image, "image/png")}
            data = {"description": "Second Post"}
            resp2 = await ac.post("/posts/", files=files, data=data)
            assert resp2.status_code == 201

            # Retrieve the first page with page_size set to 2.
            get_resp = await ac.get("/posts/", params={"page": 1, "page_size": 2})
            assert get_resp.status_code == 200, "GET posts failed for ordering test"
            posts = get_resp.json()["data"]
            # Since the GET endpoint orders posts by created_at descending,
            # the "Second Post" (created later) should appear before "First Post".
            assert posts[0]["description"] == "Second Post"
            assert posts[1]["description"] == "First Post"


@pytest.mark.asyncio
async def test_get_posts_invalid_page():
    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            get_resp = await ac.get("/posts/", params={"page": 0, "page_size": 10})
            assert get_resp.status_code == 422


@pytest.mark.asyncio
async def test_get_posts_invalid_query_params():
    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            get_resp = await ac.get(
                "/posts/", params={"page": "invalid", "page_size": "invalid"}
            )
    assert get_resp.status_code == 422


@pytest.mark.asyncio
async def test_get_posts_no_query_params():
    img_to_create = 12
    async with app.router.lifespan_context(app):
        await create_test_user()
        # Create 3 posts.
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            for i in range(img_to_create):
                image = create_test_image()
                files = {"file": ("range.png", image, "image/png")}
                data = {"description": f"No query params post {i + 1}"}
                resp = await ac.post("/posts/", files=files, data=data)
                assert resp.status_code == 201

            # Request without any query params.
            get_resp = await ac.get("/posts/")
            assert get_resp.status_code == 200
            json_data = get_resp.json()

            assert "nextPage" in json_data
            assert json_data["nextPage"] == 2
            assert "total" in json_data
            assert json_data["total"] == img_to_create
            assert "data" in json_data
            assert len(json_data["data"]) == 10  # Default page size is 10


@pytest.mark.asyncio
async def test_get_posts_page_number_out_of_range():
    async with app.router.lifespan_context(app):
        await create_test_user()
        # Create 3 posts.
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            for i in range(3):
                image = create_test_image()
                files = {"file": ("range.png", image, "image/png")}
                data = {"description": f"Out of range post {i + 1}"}
                resp = await ac.post("/posts/", files=files, data=data)
                assert resp.status_code == 201

            # Request page 2 with page_size 3 (only one page exists).
            get_resp = await ac.get("/posts/", params={"page": 2, "page_size": 3})
            assert get_resp.status_code == 200
            json_data = get_resp.json()
            # There should be no posts on the second page.
            assert json_data["data"] == []
            assert json_data["nextPage"] is None
            assert json_data["total"] == 3


@pytest.mark.asyncio
async def test_get_posts_query_by_user_id():
    user_id_1 = "00000000-0000-0000-0000-000000000001"
    user_2 = {
        "id": "00000000-0000-0000-0000-000000000002",
        "username": "testuser2",
        "email": "test2@example.com",
    }
    async with app.router.lifespan_context(app):
        await create_test_user(id=user_id_1)
        # Create 3 posts.
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            for i in range(3):
                image = create_test_image()
                files = {"file": ("range.png", image, "image/png")}
                data = {"description": f"Post by user 1 number {i + 1}"}
                resp = await ac.post("/posts/", files=files, data=data)
                assert resp.status_code == 201

            # Request all posts
            get_resp = await ac.get("/posts/")
            assert get_resp.status_code == 200
            json_data = get_resp.json()
            assert "total" in json_data
            assert json_data["total"] == 3

            # Request posts by user_id
            get_resp = await ac.get("/posts/", params={"user_id": user_id_1})
            assert get_resp.status_code == 200

            assert "total" in json_data
            assert json_data["total"] == 3
            assert "data" in json_data
            assert len(json_data["data"]) == 3

            await create_test_user(
                id=user_2["id"], username=user_2["username"], email=user_2["email"]
            )

            # Create second user
            app.dependency_overrides[current_active_user] = lambda: get_test_user(
                id=user_2["id"], username=user_2["username"], email=user_2["email"]
            )

            for i in range(3):
                image = create_test_image()
                files = {"file": ("range.png", image, "image/png")}
                data = {"description": f"Post by user 2 number {i + 1}"}
                resp = await ac.post("/posts/", files=files, data=data)
                assert resp.status_code == 201
                result = resp.json()
                assert result["post"]["userId"] == user_2["id"]

            # Request all posts
            get_resp = await ac.get("/posts/")
            assert get_resp.status_code == 200
            json_data = get_resp.json()
            assert "total" in json_data
            assert json_data["total"] == 6

            # Request posts by second user_id
            get_resp = await ac.get("/posts/", params={"user_id": user_2["id"]})
            assert get_resp.status_code == 200
            json_data = get_resp.json()
            assert "total" in json_data
            assert json_data["total"] == 3
            assert "data" in json_data
            assert len(json_data["data"]) == 3
            assert json_data["data"][0]["userId"] == user_2["id"]


@pytest.mark.asyncio
async def test_like_and_verify():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("pixel.png", image, "image/png")}
            data = {"description": "Test post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

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
            image = create_test_image()
            resp = await ac.post(
                "/posts/",
                files={"file": ("i.png", image, "image/png")},
                data={"description": "Dup"},
            )
            post_id = resp.json()["post"]["id"]

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
            image = create_test_image()
            resp = await ac.post(
                "/posts/",
                files={"file": ("u.png", image, "image/png")},
                data={"description": "Unlike"},
            )
            post_id = resp.json()["post"]["id"]
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
            image = create_test_image()
            resp = await ac.post(
                "/posts/",
                files={"file": ("v.png", image, "image/png")},
                data={"description": "No like"},
            )
            post_id = resp.json()["post"]["id"]

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


@pytest.mark.asyncio
async def test_save_post_and_verify():
    async with app.router.lifespan_context(app):
        await create_test_user()
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            image = create_test_image()
            files = {"file": ("pixel2.png", image, "image/png")}
            data = {"description": "Test save post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

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
            image = create_test_image()
            files = {"file": ("already_saved.png", image, "image/png")}
            data = {"description": "Already saved post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

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
            image = create_test_image()
            files = {"file": ("unsave.png", image, "image/png")}
            data = {"description": "Test unsave post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]
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
            image = create_test_image()
            files = {"file": ("not_saved.png", image, "image/png")}
            data = {"description": "Not saved post"}
            create_resp = await ac.post("/posts/", files=files, data=data)
            post_id = create_resp.json()["post"]["id"]

            unsave_resp = await ac.delete(f"/posts/{post_id}/save/")
            assert unsave_resp.status_code == 400


async def test_unsave_post_missing_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.delete("/posts/00000000-0000-0000-0000-000000000001/save/")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Post not found"
