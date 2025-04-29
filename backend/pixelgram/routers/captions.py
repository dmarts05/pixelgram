from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image

from pixelgram.auth import current_active_user
from pixelgram.models.user import User

captions_router = APIRouter(
    prefix="/captions",
    tags=["captions"],
)


@captions_router.post("/")
async def get_caption(
    user: User = Depends(current_active_user), file: UploadFile = File(...)
):
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

    if image.size != (128, 128):
        raise HTTPException(status_code=400, detail="Image must be 128x128 pixels.")
