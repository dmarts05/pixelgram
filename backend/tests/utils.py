from io import BytesIO
from PIL import Image
from pixelgram.models.user import User


def create_test_image(size=(128, 128), format="PNG"):
    img = Image.new("RGB", size, color="red")
    buffer = BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer

async def override_current_user():
    return User(
        id="123", username="test_user", email="test@example.com", is_active=True
    )