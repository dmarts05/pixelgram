from io import BytesIO

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
