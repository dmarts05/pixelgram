from io import BytesIO
from uuid import uuid4

import httpx
from PIL.Image import Image
from pydantic import HttpUrl

from pixelgram.settings import settings


class SupabaseStorageClient:
    """Client for uploading images to Supabase Storage."""

    def __init__(self):
        self.url = settings.supabase_url
        self.api_key = settings.supabase_service_key
        self.bucket = settings.supabase_bucket
        self.headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
        }

    async def upload(self, img: Image) -> HttpUrl:
        """
        Uploads an image to Supabase storage and returns its URL.

        Args:
            img (Image): The image object to upload.

        Returns:
            str: The URL to access the uploaded image.

        Raises:
            Exception: If the upload or signing fails.
        """
        file_data = self._image_to_png_bytes(img)
        file_id = f"{uuid4()}.png"
        upload_url = f"{self.url}/storage/v1/object/{self.bucket}/{file_id}"

        headers = self.headers.copy()
        headers["Content-Type"] = "image/png"

        async with httpx.AsyncClient() as client:
            response = await client.put(upload_url, content=file_data, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.text}")

        url = f"{self.url}/storage/v1/object/public/{self.bucket}/{file_id}"
        return HttpUrl(url)

    def _image_to_png_bytes(self, img: Image) -> bytes:
        """Convert a PIL Image object to PNG format bytes."""
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()


def get_supabase_client() -> SupabaseStorageClient:
    """
    Dependency to get the Supabase storage client.

    Returns:
        The Supabase storage client instance.
    """
    return SupabaseStorageClient()
