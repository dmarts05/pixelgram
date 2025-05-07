from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from PIL import Image
from pydantic import HttpUrl
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.user import User
from pixelgram.schemas.post import PostCreate, PostRead
from pixelgram.services.supabase_client import (
    SupabaseStorageClient,
    get_supabase_client,
)
from pixelgram.settings import Settings, get_settings
from pixelgram.utils.constants import REQUIRED_IMAGE_SIZE

posts_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@posts_router.post(
    "/",
    status_code=201,
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
                            "imageUrl": "https://example.com/image.png",
                            "userId": "00000000-0000-0000-0000-000000000001",
                            "authorUsername": "catlover123",
                            "authorEmail": "catlover123@example.com",
                            "createdAt": "2025-05-05T09:34:49.976543+00:00",
                            "likesCount": 0,
                            "likedByUser": False,
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
    supabase_client: SupabaseStorageClient = Depends(get_supabase_client),
    settings: Settings = Depends(get_settings),
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

        pr = PostRead(
            id=new_post.id,
            description=new_post.description,
            image_url=HttpUrl(new_post.image_url),
            user_id=new_post.user_id,
            author_username=user.username,
            author_email=user.email,
            created_at=new_post.created_at,
            likes_count=0,
            liked_by_user=False,
        )
        return {"post": pr.model_dump(by_alias=True)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save post: {str(e)}")


@posts_router.get(
    "/",
    summary="Retrieve paginated posts",
    description="Returns a paginated list of posts for infinite scrolling. "
    "Use query parameters to control the page and page size. You can filter by userId.",
    responses={
        200: {
            "description": "A paginated list of posts",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": "00000000-0000-0000-0000-000000000001",
                                "description": "A cat sitting on a chair",
                                "imageUrl": "https://example.com/image.png",
                                "userId": "00000000-0000-0000-0000-000000000001",
                                "authorUsername": "catlover123",
                                "authorEmail": "catlover123@example.com",
                                "createdAt": "2025-05-05T09:34:49.976543+00:00",
                                "likesCount": 23,
                                "likedByUser": True,
                            }
                        ],
                        "nextPage": 2,
                        "total": 10,
                    }
                }
            },
        },
        401: {"description": "Unauthorized"},
    },
)
async def get_posts(
    user: User = Depends(current_active_user),
    page: int = Query(1, ge=1, description="The page number to retrieve."),
    page_size: int = Query(
        10, ge=1, le=100, description="The number of posts per page."
    ),
    user_id: str | None = Query(
        None,
        description="The user ID to filter posts by.",
    ),
    db: AsyncSession = Depends(get_async_session),
):
    stmt = (
        select(Post)
        .order_by(Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .options(selectinload(Post.author), selectinload(Post.post_likes))
    )
    if user_id:
        stmt = stmt.where(Post.user_id == user_id)

    result = await db.execute(stmt)
    posts = result.scalars().all()

    count_stmt = select(func.count(Post.id))
    if user_id:
        count_stmt = count_stmt.where(Post.user_id == user_id)
    total = (await db.execute(count_stmt)).scalar() or 0
    next_page = page + 1 if (page * page_size) < total else None

    data = []
    for post in posts:
        likes_count = len(post.post_likes)
        liked_by_user = any(like.user_id == user.id for like in post.post_likes)
        pr = PostRead(
            id=post.id,
            description=post.description,
            image_url=HttpUrl(post.image_url),
            user_id=post.user_id,
            author_username=post.author.username,
            author_email=post.author.email,
            created_at=post.created_at,
            likes_count=likes_count,
            liked_by_user=liked_by_user,
        )
        data.append(pr.model_dump(by_alias=True))

    return {"data": data, "nextPage": next_page, "total": total}
