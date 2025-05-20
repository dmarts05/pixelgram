from fastapi import Depends, HTTPException
from PIL.Image import Image

from pixelgram.schemas.caption import Caption
from pixelgram.services.hf_client import HFClient, get_hf_client


class CaptionsService:
    """
    Captions service to handle caption generation.
    """

    def __init__(self, hf_client: HFClient):
        self.hf_client = hf_client

    async def generate(
        self,
        image: Image,
    ) -> Caption:
        caption = await self.hf_client.generate_caption(image)

        if not caption:
            raise HTTPException(status_code=500, detail="Failed to generate caption.")
        return Caption(caption=caption)


def get_captions_service(
    hf_client: HFClient = Depends(get_hf_client),
) -> CaptionsService:
    """
    Dependency to get the Captions service.
    """
    return CaptionsService(hf_client)
