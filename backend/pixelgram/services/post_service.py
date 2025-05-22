from typing import Optional

from fastapi import Depends, HTTPException, status
from PIL.Image import Image
from pydantic import HttpUrl
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.post_comment import PostComment
from pixelgram.models.post_like import PostLike
from pixelgram.models.post_saved import PostSaved
from pixelgram.models.user import User
from pixelgram.schemas.post import (
    PaginatedPostsResponse,
    PostCreate,
    PostRead,
    PostResponse,
)
from pixelgram.services.supabase_client import (
    SupabaseStorageClient,
    get_supabase_client,
)


class PostService:
    """
    Service for managing posts.
    """

    def __init__(self, db: AsyncSession, supabase: SupabaseStorageClient):
        self.db = db
        self.supabase = supabase

    async def create_post(
        self, user: User, description: str, image: Image
    ) -> PostResponse:
        """
        Asynchronously creates a new post for a user, including image upload and database persistence.
        Args:
            user (User): The user creating the post.
            description (str): The description of the post.
            image (Image): The image file to be uploaded and attached to the post.
        Raises:
            HTTPException: If image upload fails, post data is invalid, or database operations fail.
        Returns:
            PostResponse: The response object containing the created post's data.
        """

        # Upload image to Supabase
        try:
            image_url = await self.supabase.upload(image)
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
            self.db.add(post)
            await self.db.commit()
            await self.db.refresh(post)
        except Exception as e:
            await self.db.rollback()
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
                comments_count=0,
                commented_by_user=False,
                saved_by_user=False,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid post data: {str(e)}",
            )

        return PostResponse(post=pr)

    async def get_posts(
        self,
        user: User,
        page: int = 1,
        page_size: int = 10,
        user_id: Optional[str] = None,
    ) -> PaginatedPostsResponse:
        """
        Retrieve paginated posts with additional metadata for the given user.
        Args:
            user (User): The current authenticated user requesting the posts.
            page (int, optional): The page number for pagination. Defaults to 1.
            page_size (int, optional): The number of posts per page. Defaults to 10.
            user_id (Optional[str], optional): If provided, filters posts by this user ID.
        Returns:
            PaginatedPostsResponse: An object containing the list of posts with metadata,
                the next page number (if available), and the total number of posts.
        The response includes, for each post:
            - Post details (id, description, image_url, user_id, author info, created_at)
            - Number of likes and comments
            - Whether the current user has liked, commented, or saved the post
        Raises:
            Any exceptions raised by the underlying database operations.
        """

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
        result = await self.db.execute(stmt)
        posts = result.scalars().all()
        post_ids = [post.id for post in posts]

        # Count total posts for pagination and determine next page
        count_stmt = select(func.count(Post.id))
        if user_id:
            count_stmt = count_stmt.where(Post.user_id == user_id)
        total = (await self.db.execute(count_stmt)).scalar() or 0
        next_page = page + 1 if (page * page_size) < total else None

        # Fetch likes count for each post
        likes_stmt = (
            select(PostLike.post_id, func.count(PostLike.user_id))
            .where(PostLike.post_id.in_(post_ids))
            .group_by(PostLike.post_id)
        )
        likes_result = await self.db.execute(likes_stmt)
        likes_map = {post_id: count for post_id, count in likes_result.all()}

        # Fetch liked posts by the user
        liked_stmt = select(PostLike.post_id).where(
            PostLike.post_id.in_(post_ids), PostLike.user_id == user.id
        )
        liked_result = await self.db.execute(liked_stmt)
        liked_post_ids = {post_id for (post_id,) in liked_result.all()}

        # Fetch comments count for each post
        comments_stmt = (
            select(PostComment.post_id, func.count(PostComment.id))
            .where(PostComment.post_id.in_(post_ids))
            .group_by(PostComment.post_id)
        )
        comments_result = await self.db.execute(comments_stmt)
        comments_map = {post_id: count for post_id, count in comments_result.all()}

        # Fetch commented posts by the user
        commented_stmt = select(PostComment.post_id).where(
            PostComment.post_id.in_(post_ids), PostComment.user_id == user.id
        )
        commented_result = await self.db.execute(commented_stmt)
        commented_post_ids = {post_id for (post_id,) in commented_result.all()}

        # Fetch saved posts by the user
        saved_stmt = select(PostSaved.post_id).where(
            PostSaved.post_id.in_(post_ids), PostSaved.user_id == user.id
        )
        saved_result = await self.db.execute(saved_stmt)
        saved_post_ids = {post_id for (post_id,) in saved_result.all()}

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
                comments_count=comments_map.get(post.id, 0),
                commented_by_user=post.id in commented_post_ids,
                saved_by_user=post.id in saved_post_ids,
            )
            data.append(pr.model_dump(by_alias=True))
        return PaginatedPostsResponse(data=data, nextPage=next_page, total=total)

    async def delete_post(self, post: Post) -> None:
        """
        Asynchronously deletes a post and its associated image.
        This method performs the following actions:
        1. Deletes the image associated with the given post from Supabase storage.
        2. Deletes the post record from the database.
        Args:
            post (Post): The post instance to be deleted.
        Raises:
            HTTPException: If image deletion from Supabase fails, raises an HTTP 500 error with details.
        """

        # Delete the image from Supabase
        try:
            await self.supabase.delete(HttpUrl(post.image_url))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Image deletion from storage failed.",
            )

        # Delete the post from database
        await self.db.delete(post)
        await self.db.commit()

    async def delete_all_from(self, user: User) -> None:
        """
        Asynchronously deletes all posts created by the specified user, including their associated images.
        Args:
            user (User): The user whose posts are to be deleted.
        Returns:
            None
        """

        # Fetch all posts by the user
        stmt = select(Post).where(Post.user_id == user.id)
        result = await self.db.execute(stmt)
        posts = result.scalars().all()

        # Delete each post and its associated image
        for post in posts:
            await self.delete_post(post)


def get_post_service(
    db: AsyncSession = Depends(get_async_session),
    supabase_client: SupabaseStorageClient = Depends(get_supabase_client),
) -> PostService:
    """
    Dependency to get the PostService instance.
    """
    return PostService(db, supabase_client)
