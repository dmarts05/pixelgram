from uuid import UUID

from fastapi import Depends, HTTPException, status
from pydantic import HttpUrl
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pixelgram.db import get_async_session
from pixelgram.models.post import Post
from pixelgram.models.post_comment import PostComment
from pixelgram.models.post_like import PostLike
from pixelgram.models.post_saved import PostSaved
from pixelgram.schemas.post import PaginatedPostsResponse, PostRead


class SavedService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_post(self, post_id: UUID, user_id: UUID) -> None:
        """
        Saves a post for a user if it has not already been saved.
        Args:
            post_id (UUID): The unique identifier of the post to be saved.
            user_id (UUID): The unique identifier of the user saving the post.
        Raises:
            HTTPException: If the post has already been saved by the user (HTTP 409 Conflict).
        Returns:
            None
        """

        # Check if user has already saved the post
        stmt = select(PostSaved).where(
            PostSaved.post_id == post_id, PostSaved.user_id == user_id
        )

        if (await self.db.execute(stmt)).scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Post already saved"
            )

        # Add save
        self.db.add(PostSaved(post_id=post_id, user_id=user_id))
        await self.db.commit()

    async def unsave_post(self, post_id: UUID, user_id: UUID) -> None:
        """
        Asynchronously removes a saved post for a given user.
        Args:
            post_id (UUID): The unique identifier of the post to unsave.
            user_id (UUID): The unique identifier of the user performing the unsave action.
        Raises:
            HTTPException: If the post was not previously saved by the user, raises a 400 Bad Request error.
        Returns:
            None
        """

        # Delete save
        delete_stmt = (
            delete(PostSaved)
            .where(PostSaved.post_id == post_id, PostSaved.user_id == user_id)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.db.execute(delete_stmt)
        # If save was not deleted, it means the user didn't save the post in the first place
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Post not saved"
            )
        await self.db.commit()

    async def get_saved_posts(
        self, user_id: UUID, page: int = 1, page_size: int = 10
    ) -> PaginatedPostsResponse:
        """
        Retrieve a paginated list of posts saved by a specific user, including metadata such as likes, comments, and user interactions.
        Args:
            user_id (UUID): The unique identifier of the user whose saved posts are to be retrieved.
            page (int, optional): The page number for pagination. Defaults to 1.
            page_size (int, optional): The number of posts per page. Defaults to 10.
        Returns:
            PaginatedPostsResponse: An object containing the paginated list of saved posts, the next page number (if any), and the total count of saved posts.
        The response includes for each post:
            - Post details (id, description, image_url, user_id, author info, created_at)
            - Number of likes and comments
            - Whether the current user has liked or commented on the post
            - Whether the post is saved by the user (always True in this context)
        """

        # Get all post IDs saved by the current user
        saved_posts_ids_stmt = select(PostSaved.post_id).where(
            PostSaved.user_id == user_id
        )
        result = await self.db.execute(saved_posts_ids_stmt)
        saved_posts_ids = [row[0] for row in result.fetchall()]

        if not saved_posts_ids:
            return PaginatedPostsResponse(data=[], nextPage=None, total=0)

        stmt = (
            select(Post)
            .where(Post.id.in_(saved_posts_ids))
            .order_by(Post.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .options(
                selectinload(Post.author),
                selectinload(Post.post_likes),
                selectinload(Post.post_comments),
            )
        )

        result = await self.db.execute(stmt)
        saved_posts = result.scalars().all()

        # Count total saved posts for pagination and determine next page
        count_stmt = select(func.count(PostSaved.id))
        if user_id:
            count_stmt = count_stmt.where(PostSaved.user_id == user_id)
        total = (await self.db.execute(count_stmt)).scalar() or 0
        next_page = page + 1 if (page * page_size) < total else None

        # Fetch likes count for each post
        likes_stmt = (
            select(PostLike.post_id, func.count(PostLike.user_id))
            .where(PostLike.post_id.in_(saved_posts_ids))
            .group_by(PostLike.post_id)
        )
        likes_result = await self.db.execute(likes_stmt)
        likes_map = {post_id: count for post_id, count in likes_result.all()}

        # Fetch liked posts by the user
        liked_stmt = select(PostLike.post_id).where(
            PostLike.post_id.in_(saved_posts_ids), PostLike.user_id == user_id
        )
        liked_result = await self.db.execute(liked_stmt)
        liked_post_ids = {post_id for (post_id,) in liked_result.all()}

        # Fetch comments count for each post
        comments_stmt = (
            select(PostComment.post_id, func.count(PostComment.id))
            .where(PostComment.post_id.in_(saved_posts_ids))
            .group_by(PostComment.post_id)
        )
        comments_result = await self.db.execute(comments_stmt)
        comments_map = {post_id: count for post_id, count in comments_result.all()}

        # Fetch commented posts by the user
        commented_stmt = select(PostComment.post_id).where(
            PostComment.post_id.in_(saved_posts_ids), PostComment.user_id == user_id
        )
        commented_result = await self.db.execute(commented_stmt)
        commented_post_ids = {post_id for (post_id,) in commented_result.all()}

        # Construct the response
        data = []
        for saved_post in saved_posts:
            pr = PostRead(
                id=saved_post.id,
                description=saved_post.description,
                image_url=HttpUrl(saved_post.image_url),
                user_id=saved_post.user_id,
                author_username=saved_post.author.username,
                author_email=saved_post.author.email,
                created_at=saved_post.created_at,
                likes_count=likes_map.get(saved_post.id, 0),
                liked_by_user=saved_post.id in liked_post_ids,
                comments_count=comments_map.get(saved_post.id, 0),
                commented_by_user=saved_post.id in commented_post_ids,
                saved_by_user=True,
            )
            data.append(pr.model_dump(by_alias=True))

        return PaginatedPostsResponse(data=data, nextPage=next_page, total=total)


def get_saved_service(db: AsyncSession = Depends(get_async_session)) -> SavedService:
    """
    Dependency to get the SavedService instance.
    """
    return SavedService(db)
