from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.models.post import Post
from pixelgram.auth import current_active_user
from pixelgram.models.user import User
from pixelgram.services.supabase_client import SupabaseStorageClient
from pixelgram.db import get_async_session

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

    if image.size != (128, 128):
        raise HTTPException(status_code=400, detail="Image must be 128x128 pixels.")

    try:
        supabase_client = SupabaseStorageClient()
        image_url = await supabase_client.upload(image)
        
        new_post = Post(
            description=description,
            image_url=image_url,
            user_id=user.id,
        )
        
        print(user.id)
        
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
        
        return {
            "post": {
                "id": new_post.id,
                "description": new_post.description,
                "image_url": new_post.image_url,
                "created_at": new_post.created_at,
                "user_id": new_post.user_id,
            }
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save post.")