from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.user import User
from pixelgram.schemas.post import PostCreate, PostRead
from pixelgram.services.supabase_client import SupabaseStorageClient
from pixelgram.settings import settings

REQUIRED_IMAGE_SIZE = (128, 128)  # Required image size in pixels

posts_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@posts_router.post(
    "/",
    summary="Creates a pixelart post",
    description="Takes an uploaded image (must be 128x128 pixels) and its description and saves it as a pixelart post.",
    responses={
        201: {
            "description": "Post successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "post": {
                            "id": 1,
                            "description": "A cat sitting on a chair",
                            "image_url": "https://example.com/image.png",
                        }
                    }
                }
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
async def post_pixelart(
    user: User = Depends(current_active_user),
    file: UploadFile = File(...),
    description: str = Form(...),
    db: AsyncSession = Depends(get_async_session),
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

    if len(image_bytes) > settings.max_img_mb_size * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"Image exceeds {settings.max_img_mb_size}MB size limit.",
        )

    if image.size != REQUIRED_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Image must be {REQUIRED_IMAGE_SIZE[0]}x{REQUIRED_IMAGE_SIZE[1]} pixels.",
        )

    try:
        supabase_client = SupabaseStorageClient()
        image_url = await supabase_client.upload(image)

        post_data = PostCreate(
            description=description,
            image_url=image_url,
            user_id=user.id,
        )

        new_post = Post(
            description=post_data.description,
            image_url=str(post_data.image_url),
            user_id=post_data.user_id,
        )

        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)

        return {"post": PostRead.model_validate(new_post).model_dump()}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save post: {str(e)}")
