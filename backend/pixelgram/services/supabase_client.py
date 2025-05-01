import httpx
from uuid import uuid4
from io import BytesIO
from PIL.Image import Image
from pixelgram.settings import settings


class SupabaseStorageClient:
    """Client for uploading images to Supabase Storage."""
    
    def __init__(self):
        self.url = settings.supabase_url.rstrip("/")
        self.api_key = settings.supabase_key
        self.bucket = settings.supabase_bucket
        self.headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
        }

    async def upload(self, img: Image) -> str:
        """
        Uploads an image to Supabase storage.

        Args:
            img (Image): The image object to upload.

        Returns:
            str: The public URL of the uploaded image.

        Raises:
            Exception: If the upload to Supabase fails.

        Notes:
            The image is converted to PNG format before uploading.
            A unique filename is generated using UUID.
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

        return f"{self.url}/storage/v1/object/public/{self.bucket}/{file_id}"

    def _image_to_png_bytes(self, img: Image) -> bytes:
        """
        Convert a PIL Image object to PNG format bytes.

        Args:
            img (Image): PIL Image object to be converted.

        Returns:
            bytes: The image data in PNG format as bytes.
        """
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()
