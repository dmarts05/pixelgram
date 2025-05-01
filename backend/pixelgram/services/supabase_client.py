import httpx
from uuid import uuid4
from io import BytesIO
from PIL.Image import Image
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

    async def upload(self, img: Image) -> str:
        """
        Uploads an image to Supabase storage and returns a signed URL (private access).

        Args:
            img (Image): The image object to upload.

        Returns:
            str: A signed URL to access the uploaded image.

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

        signed_url = await self._generate_signed_url(file_id, expires_in=3600)
        return signed_url

    async def _generate_signed_url(self, file_path: str, expires_in: int = 3600) -> str:
        """
        Generates a signed URL to access a private file.

        Args:
            file_path (str): The file path inside the bucket.
            expires_in (int): Time in seconds the URL is valid (default: 3600s).

        Returns:
            str: A signed URL for accessing the file.
        """
        url = f"{self.url}/storage/v1/object/sign/{self.bucket}/{file_path}"
        json_body = {"expiresIn": expires_in}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=json_body)

        if response.status_code != 200:
            print(
                f"Failed to generate signed URL: {response.status_code} - {response.text}"
            )
            raise Exception(f"Failed to generate signed URL: {response.text}")

        signed_path = response.json().get("signedURL")
        return f"{self.url}{signed_path}"

    def _image_to_png_bytes(self, img: Image) -> bytes:
        """Convert a PIL Image object to PNG format bytes."""
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()
