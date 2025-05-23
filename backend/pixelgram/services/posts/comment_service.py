from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from pixelgram.db import get_async_session
from pixelgram.models.post_comment import PostComment
from pixelgram.models.user import User
from pixelgram.schemas.post_comment import (
    CommentResponse,
    PaginatedCommentsResponse,
    PostCommentRead,
)


class CommentService:
    """
    Service for handling post comments.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_post_id(
        self, post_id: UUID, page: int, page_size: int, solicitor_id: UUID
    ) -> PaginatedCommentsResponse:
        """
        Retrieve paginated comments for a specific post.

        Args:
            post_id (UUID): The unique identifier of the post to retrieve comments for.
            page (int): The current page number for pagination.
            page_size (int): The number of comments to retrieve per page.
            solicitor_id (UUID): The ID of the user making the request, used to determine comment ownership.

        Returns:
            PaginatedCommentsResponse: An object containing the list of comments, the next page number (if any), and the total number of comments.

        Notes:
            - Comments are ordered by creation date in descending order (most recent first).
            - Each comment includes author information and a flag indicating if it was made by the requesting user.
        """

        stmt = (
            select(PostComment)
            .where(PostComment.post_id == post_id)
            .order_by(PostComment.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .options(selectinload(PostComment.user))
        )
        result = await self.db.execute(stmt)
        comments = result.scalars().all()

        # Count total comments for pagination and determine next page
        count_stmt = select(func.count(PostComment.id)).where(
            PostComment.post_id == post_id
        )
        total = (await self.db.execute(count_stmt)).scalar() or 0
        next_page = page + 1 if (page * page_size) < total else None

        # Construct the response
        data = []
        for c in comments:
            cr = PostCommentRead(
                id=c.id,
                post_id=c.post_id,
                user_id=c.user_id,
                author_username=c.user.username,
                author_email=c.user.email,
                content=c.content,
                created_at=c.created_at,
                by_user=(c.user_id == solicitor_id),
            )
            data.append(cr.model_dump(by_alias=True))

        return PaginatedCommentsResponse(data=data, nextPage=next_page, total=total)

    async def post_comment(
        self, post_id: UUID, user: User, content: str
    ) -> CommentResponse:
        """
        Create and persist a new comment for a given post.
        Args:
            post_id (UUID): The unique identifier of the post to comment on.
            user (User): The user creating the comment.
            content (str): The content of the comment.
        Returns:
            CommentResponse: The response object containing the created comment details.
        Raises:
            HTTPException: If the comment data is invalid or cannot be created.
        """

        # Validate comment content and create comment
        try:
            comment = PostComment(
                post_id=post_id,
                user_id=user.id,
                content=content,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid comment data: {str(e)}",
            )
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)

        # Return the created comment
        cr = PostCommentRead(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            author_username=user.username,
            author_email=user.email,
            content=comment.content,
            created_at=comment.created_at,
            by_user=True,
        )
        return CommentResponse(comment=cr)

    async def delete_comment(self, comment: PostComment) -> None:
        """
        Asynchronously deletes a given comment from the database.
        Args:
            comment (PostComment): The comment instance to be deleted.
        Returns:
            None
        """

        # Delete the comment
        await self.db.delete(comment)
        await self.db.commit()


def get_comment_service(
    db: AsyncSession = Depends(get_async_session),
) -> CommentService:
    """
    Dependency to get the PostComment service.
    """
    return CommentService(db)
