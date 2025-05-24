from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from PIL import Image

from pixelgram.auth import current_active_user
from pixelgram.limiter import limiter
from pixelgram.models.user import User
from pixelgram.schemas.caption import Caption
from pixelgram.services.captions_service import CaptionsService, get_captions_service
from pixelgram.utils.constants import REQUIRED_IMAGE_SIZE

captions_router = APIRouter(
    prefix="/captions",
    tags=["captions"],
)


@captions_router.post(
    "/",
    summary="Generate a caption for an image",
    description="Takes an uploaded image (must be 128x128 pixels) and returns a generated caption. Only image files are allowed.",
    responses={
        200: {
            "description": "Caption successfully generated",
            "content": {
                "application/json": {"example": {"caption": "A cat sitting on a chair"}}
            },
        },
        400: {
            "description": "Invalid input (e.g., wrong size or type)",
            "content": {
                "application/json": {
                    "example": {"detail": "Image must be 128x128 pixels."}
                }
            },
        },
        401: {"description": "Unauthorized"},
    },
)
@limiter.limit("30/15minutes")
async def get_caption(
    request: Request,
    user: User = Depends(current_active_user),
    file: UploadFile = File(...),
    captions_service: CaptionsService = Depends(get_captions_service),
) -> Caption:
    content_type = file.content_type
    if not content_type or not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid content type. Only image files are allowed.",
        )

    image_bytes = await file.read()

    try:
        image = Image.open(BytesIO(image_bytes))
    except Exception as e:
        print(f"Error opening image: {e}")
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file.")

    if image.size != REQUIRED_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image must be 128x128 pixels.")

    return await captions_service.generate(image)
