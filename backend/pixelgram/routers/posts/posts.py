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
from sqlalchemy.ext.asyncio import AsyncSession

from pixelgram.auth import current_active_user
from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.user import User
from pixelgram.routers.posts.comments import posts_comments_router
from pixelgram.routers.posts.likes import post_likes_router
from pixelgram.routers.posts.saved import saved_posts_router
from pixelgram.schemas.post import (
    PaginatedPostsResponse,
    PostResponse,
)
from pixelgram.services.post_service import PostService, get_post_service
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

posts_router.include_router(posts_comments_router)
posts_router.include_router(post_likes_router)
posts_router.include_router(saved_posts_router)


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
    post_service: PostService = Depends(get_post_service),
) -> PostResponse:
    # Check if file is an image
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

    # Check if image does not exceed the maximum size and dimensions
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

    return await post_service.create_post(
        image=image,
        description=description,
        user=user,
    )


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
                                "commentsCount": 5,
                                "commentedByUser": True,
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
    post_service: PostService = Depends(get_post_service),
) -> PaginatedPostsResponse:
    return await post_service.get_posts(
        user=user,
        page=page,
        page_size=page_size,
        user_id=user_id,
    )


@posts_router.delete(
    "/{post_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a post",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Post deleted"},
        status.HTTP_404_NOT_FOUND: {"description": "Post not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"},
    },
)
async def delete_post(
    post_id: UUID = Path(..., description="The ID of the post"),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
    supabase_client: SupabaseStorageClient = Depends(get_supabase_client),
    post_service: PostService = Depends(get_post_service),
):
    # Check if post exists
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if user is the owner of the post
    if str(post.user_id) != str(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not post owner"
        )

    # Delete the post
    await post_service.delete_post(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
