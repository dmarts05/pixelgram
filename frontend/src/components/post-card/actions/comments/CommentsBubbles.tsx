import React from "react";
import { PostComment } from "../../../../types/post-comment";
import InfiniteScrollIntersectionObserver from "../../../InfiniteScrollIntersectionObserver";
import Comment from "./Comment";

type CommentsBubblesProps = {
    comments: PostComment[];
    hasNextPage: boolean;
    isFetchingNextPage: boolean;
    fetchNextPage: () => void;
    refetchPosts: () => void;
    refetchComments: () => void;
};

function CommentsBubbles({
    comments,
    hasNextPage,
    isFetchingNextPage,
    fetchNextPage,
    refetchPosts,
    refetchComments,
}: CommentsBubblesProps): React.ReactNode {
    return (
        <div className="flex flex-col flex-grow h-[60vh] overflow-y-auto pb-1 gap-4">
            {comments.map((comment) => (
                <React.Fragment key={comment.id}>
                    <Comment
                        postId={comment.postId}
                        commentId={comment.id}
                        authorUsername={comment.authorUsername}
                        content={comment.content}
                        createdAt={comment.createdAt}
                        byUser={comment.byUser}
                        refetchPosts={refetchPosts}
                        refetchComments={refetchComments}
                    />
                </React.Fragment>
            ))}
            <InfiniteScrollIntersectionObserver
                onIntersect={(): void => {
                    if (hasNextPage) {
                        fetchNextPage();
                    }
                }}
                hasNextPage={hasNextPage}
                isFetchingNextPage={isFetchingNextPage}
                className="flex justify-center items-center pb-3 pt-[5px]"
                noMoreItemsMessage="No more comments to load."
            />
        </div>
    );
}

export default CommentsBubbles;
