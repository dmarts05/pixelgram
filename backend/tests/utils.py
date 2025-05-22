from io import BytesIO
from typing import Optional

from PIL import Image

from pixelgram.db import get_async_session
from pixelgram.models.user import User


def create_test_image(size=(128, 128), format="PNG", color="blue") -> BytesIO:
    img = Image.new("RGB", size, color=color)
    buffer = BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer


def get_test_user(
    id: str = "00000000-0000-0000-0000-000000000001",
    username: str = "test",
    email: str = "test@example.com",
    hashed_password: str = "hashed_password",
    is_active: bool = True,
) -> User:
    return User(
        id=id,
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_active=is_active,
    )


async def create_test_user(
    id: str = "00000000-0000-0000-0000-000000000001",
    username: str = "test",
    email: str = "test@example.com",
    hashed_password: str = "hashed_password",
    is_active: bool = True,
):
    async for session in get_async_session():
        async with session.begin():
            session.add(get_test_user(id, username, email, hashed_password, is_active))
            await session.commit()


async def create_test_post(
    user_id: str = "00000000-0000-0000-0000-000000000001",
    content: str = "Test post",
    image_size=(128, 128),
    image_format="PNG",
    image_color="blue",
    description: Optional[str] = None,
    client=None,
) -> str:
    """
    Create a test post for a given user. Returns the post ID.
    If client is provided, uses it to make the request (for HTTPX AsyncClient usage).
    """
    if description is None:
        description = content
    image = create_test_image(size=image_size, format=image_format, color=image_color)
    files = {"file": ("test.png", image, f"image/{image_format.lower()}")}
    data = {"description": description}
    if client is not None:
        response = await client.post("/posts/", files=files, data=data)
        response.raise_for_status()
        return response.json()["post"]["id"]
    # If no client is provided, raise error (enforce usage pattern)
    raise ValueError("A client (AsyncClient) must be provided to create a test post.")
