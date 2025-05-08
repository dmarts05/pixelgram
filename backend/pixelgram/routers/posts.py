from io import BytesIO
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    Response,
    UploadFile,
    status,
)
from PIL import Image
from pydantic import HttpUrl
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.post_like import PostLike
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
    status_code=status.HTTP_201_CREATED,
    summary="Creates a pixelart post",
    description="Takes an uploaded image (must be 128x128 pixels) and its description and saves it as a pixelart post.",
    responses={
        status.HTTP_201_CREATED: {
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
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input (e.g., wrong size or type)",
            "content": {
                "application/json": {
                    "example": {"detail": "Image must be 128x128 pixels."}
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
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
    # Check if the file is an image
    content_type = file.content_type
    if not content_type or not content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content type. Only image files are allowed.",
        )
    image_bytes = await file.read()
    try:
        image = Image.open(BytesIO(image_bytes))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or corrupted image file.",
        )

    # Check if the image does not exceed the maximum size and dimensions
    if len(image_bytes) > settings.max_img_mb_size * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image exceeds {settings.max_img_mb_size}MB size limit.",
        )
    if image.size != REQUIRED_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image must be {REQUIRED_IMAGE_SIZE[0]}x{REQUIRED_IMAGE_SIZE[1]} pixels.",
        )

    # Upload image to Supabase
    try:
        image_url = await supabase_client.upload(image)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image upload failed: {str(e)}",
        )

    # Create a new post and save it to the database
    try:
        pc = PostCreate(
            description=description,
            image_url=image_url,
            user_id=user.id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid post data: {str(e)}",
        )
    post = Post(
        description=pc.description,
        image_url=str(pc.image_url),
        user_id=pc.user_id,
    )
    try:
        db.add(post)
        await db.commit()
        await db.refresh(post)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save post: {str(e)}",
        )

    # Return the created post
    try:
        pr = PostRead(
            id=post.id,
            description=post.description,
            image_url=HttpUrl(post.image_url),
            user_id=post.user_id,
            author_username=user.username,
            author_email=user.email,
            created_at=post.created_at,
            likes_count=0,
            liked_by_user=False,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid post data: {str(e)}",
        )

    return {"post": pr.model_dump(by_alias=True)}


@posts_router.get(
    "/",
    summary="Retrieve paginated posts",
    description="Returns a paginated list of posts for infinite scrolling. "
    "Use query parameters to control the page and page size. You can filter by userId.",
    responses={
        status.HTTP_200_OK: {
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
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def get_posts(
    user: User = Depends(current_active_user),
    page: int = Query(1, ge=1, description="The page number to retrieve."),
    page_size: int = Query(
        10, ge=1, le=100, description="The number of posts per page."
    ),
    user_id: str | None = Query(None, description="The user ID to filter posts by."),
    db: AsyncSession = Depends(get_async_session),
):
    # Get posts with pagination and filter by user_id if provided
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
    post_ids = [post.id for post in posts]

    # Count total posts for pagination and determine next page
    count_stmt = select(func.count(Post.id))
    if user_id:
        count_stmt = count_stmt.where(Post.user_id == user_id)
    total = (await db.execute(count_stmt)).scalar() or 0
    next_page = page + 1 if (page * page_size) < total else None

    # Fetch likes count for each post
    likes_stmt = (
        select(PostLike.post_id, func.count(PostLike.user_id))
        .where(PostLike.post_id.in_(post_ids))
        .group_by(PostLike.post_id)
    )
    likes_result = await db.execute(likes_stmt)
    likes_map = {post_id: count for post_id, count in likes_result.all()}

    # Fetch liked posts by the user
    liked_stmt = select(PostLike.post_id).where(
        PostLike.post_id.in_(post_ids), PostLike.user_id == user.id
    )
    liked_result = await db.execute(liked_stmt)
    liked_post_ids = {post_id for (post_id,) in liked_result.all()}

    # Construct the response
    data = []
    for post in posts:
        pr = PostRead(
            id=post.id,
            description=post.description,
            image_url=HttpUrl(post.image_url),
            user_id=post.user_id,
            author_username=post.author.username,
            author_email=post.author.email,
            created_at=post.created_at,
            likes_count=likes_map.get(post.id, 0),
            liked_by_user=post.id in liked_post_ids,
        )
        data.append(pr.model_dump(by_alias=True))
    return {"data": data, "nextPage": next_page, "total": total}


@posts_router.post(
    "/{post_id}/like/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Like a post",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Post liked"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
        status.HTTP_409_CONFLICT: {"description": "Already liked"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def like_post(
    post_id: UUID = Path(..., description="The ID of the post to like"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Check if the post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if the user has already liked the post
    stmt = select(PostLike).where(
        PostLike.post_id == post_id, PostLike.user_id == user.id
    )
    if (await db.execute(stmt)).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Post already liked"
        )

    # Add like
    db.add(PostLike(post_id=post_id, user_id=user.id))
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@posts_router.delete(
    "/{post_id}/like/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unlike a post",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Post unliked"},
        status.HTTP_400_BAD_REQUEST: {"description": "Post not liked"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def unlike_post(
    post_id: UUID = Path(..., description="The ID of the post to unlike"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Check if the post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Delete like
    delete_stmt = (
        delete(PostLike)
        .where(PostLike.post_id == post_id, PostLike.user_id == user.id)
        .execution_options(synchronize_session="fetch")
    )
    result = await db.execute(delete_stmt)
    # If like was not deleted, it means the user didn't like the post in the first place
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Post not liked"
        )
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
