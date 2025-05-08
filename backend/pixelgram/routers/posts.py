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

        post_read = PostRead(
            id=new_post.id,
            description=new_post.description,
            image_url=HttpUrl(new_post.image_url),
            user_id=new_post.user_id,
            author_username=user.username,
            author_email=user.email,
            created_at=new_post.created_at,
        )
        return {"post": post_read.model_dump(by_alias=True)}
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
    db: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1, description="The page number to retrieve."),
    page_size: int = Query(
        10, ge=1, le=100, description="The number of posts per page."
    ),
    user_id: str | None = Query(
        None,
        description="The user ID to filter posts by.",
    ),
):
    # Query posts ordered by creation date
    stmt = (
        select(Post)
        .order_by(Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .options(selectinload(Post.author))
    )

    if user_id:
        stmt = stmt.where(Post.user_id == user_id)

    result = await db.execute(stmt)
    posts = result.scalars().all()

    # Count total posts for pagination metadata
    count_stmt = select(func.count(Post.id))
    if user_id:
        count_stmt = count_stmt.where(Post.user_id == user_id)

    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # Determine next page for infinite scrolling; returns None if no more pages.
    next_page = page + 1 if (page * page_size) < total else None

    post_reads = [
        PostRead(
            id=post.id,
            description=post.description,
            image_url=HttpUrl(post.image_url),
            user_id=post.user_id,
            author_username=post.author.username,
            author_email=post.author.email,
            created_at=post.created_at,
        )
        for post in posts
    ]
    return {
        "data": [post.model_dump(by_alias=True) for post in post_reads],
        "nextPage": next_page,
        "total": total,
    }


@posts_router.post(
    "/{post_id}/save",
    summary="Save a specific post by ID",
    description="Saves a post for the current user.",
    responses={
        200: {
            "description": "Post saved successfully",
            "content": {
                "application/json": {"example": {"message": "Post saved successfully"}}
            },
        },
        401: {"description": "Unauthorized"},
        404: {"description": "Post not found"},
    },
)
async def save_post():
    """
    Save a post for the current user.
    """
    pass


@posts_router.delete(
    "/{post_id}/unsave",
    summary="Unsave a specific post by ID",
    description="Removes a post from the saved list for the current user.",
    responses={
        200: {
            "description": "Post unsaved successfully",
            "content": {
                "application/json": {
                    "example": {"message": "Post unsaved successfully"}
                }
            },
        },
        401: {"description": "Unauthorized"},
        404: {"description": "Post not found"},
    },
)
async def unsave_post():
    """
    Remove a post from the saved list for the current user.
    """
    pass


@posts_router.get(
    "/saved",
    summary="Get all saved posts",
    description="Retrieves all posts saved by the current user.",
    responses={
        200: {
            "description": "List of saved posts",
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
                                "authorEmail": "catlover123@email.com",
                            }
                        ]
                    }
                }
            },
        }
    },
)
async def get_saved_posts():
    """
    Get all saved posts for the current user.
    """
    pass
