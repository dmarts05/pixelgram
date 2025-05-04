from io import BytesIO

from PIL import Image

from pixelgram.db import get_async_session
from pixelgram.models.user import User

has_test_user_been_created = False


def create_test_image(size=(128, 128), format="PNG", color="blue") -> BytesIO:
    img = Image.new("RGB", size, color=color)
    buffer = BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer


def get_test_user() -> User:
    return User(
        id="00000000-0000-0000-0000-000000000001",
        username="test",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )


async def create_test_user():
    global has_test_user_been_created
    if has_test_user_been_created:
        return
    async for session in get_async_session():
        async with session.begin():
            session.add(get_test_user())
            await session.commit()
            has_test_user_been_created = True
