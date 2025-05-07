import base64
from io import BytesIO

from huggingface_hub import InferenceClient
from PIL.Image import Image

from pixelgram.settings import settings


class HFClient:
    def __init__(self):
        self.client = InferenceClient(
            provider="hf-inference", api_key=settings.hf_token
        )
        self.model = settings.hf_img2txt_model

    async def generate_caption(self, image: Image) -> str:
        # Convert to PNG bytes
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        png_bytes = buffer.getvalue()

        # Codify as base64
        base64_image = base64.b64encode(png_bytes).decode("utf-8")
        data_uri = f"data:image/png;base64,{base64_image}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Give me a caption for this"},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=500,
            top_p=0.7,
        )
        
        if not completion.choices or not completion.choices[0].message:
            raise ValueError("No valid response from the model.")
        
        if not completion.choices[0].message.content:
            raise ValueError("No content in the response from the model.")

        return str(completion.choices[0].message.content)


def get_hf_client() -> HFClient:
    return HFClient()
