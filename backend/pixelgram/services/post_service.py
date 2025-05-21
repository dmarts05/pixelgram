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

    async def create_post(self, user: User, description: str, image: Image):
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

    async def delete_post(self, post: Post):
        # Delete the post from database
        await self.db.delete(post)
        await self.db.commit()

        # Delete the image from Supabase
        try:
            await self.supabase.delete(HttpUrl(post.image_url))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Image deletion failed: {str(e)}",
            )


def get_post_service(
    db: AsyncSession = Depends(get_async_session),
    supabase_client: SupabaseStorageClient = Depends(get_supabase_client),
) -> PostService:
    """
    Dependency to get the PostService instance.
    """
    return PostService(db, supabase_client)
