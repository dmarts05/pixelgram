import httpx

from pixelgram.settings import settings


class HuggingFaceClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.hf_token}",
        }
        self.base_url = "https://api-inference.huggingface.co/models/"

    async def generate_caption(self, image_bytes: bytes) -> str:
        headers = self.headers.copy()
        headers["Content-Type"] = "application/octet-stream"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url + settings.hf_img2txt_model,
                headers=self.headers,
                content=image_bytes,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("generated_text", "No caption found.")
