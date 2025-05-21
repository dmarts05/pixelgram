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

    async def delete(self, file_url: HttpUrl) -> bool:
        """
        Deletes an image from Supabase storage based on its URL.

        Args:
            file_url (HttpUrl): The URL of the image to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.

        Raises:
            ValueError: If the URL format is invalid.
            Exception: If the deletion fails with an error other than 404.
        """
        # Extract file_id from the URL
        prefix = f"public/{self.bucket}/"
        url_str = str(file_url)
        if prefix not in url_str:
            raise ValueError(f"Invalid Supabase URL format: {file_url}")
        file_id = url_str.split(prefix, 1)[1]

        delete_url = f"{self.url}/storage/v1/object/{self.bucket}/{file_id}"

        async with httpx.AsyncClient() as client:
            response = await client.delete(delete_url, headers=self.headers)

        # 200 means successful deletion
        if response.status_code == 200:
            return True
        # 404 means file not found, which we'll treat as a "successful" deletion
        elif response.status_code == 404:
            return True
        # Any other status code is an error
        else:
            raise Exception(f"Deletion failed: {response.text}")

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
