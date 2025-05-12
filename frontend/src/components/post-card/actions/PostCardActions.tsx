import {
    InfiniteData,
    QueryObserverResult,
    RefetchOptions,
} from "@tanstack/react-query";
import { PostPage } from "../../PostsGrid";
import CommentsButton from "./CommentsButton";
import LikeButton from "./LikeButton";
import SaveButton from "./SaveButton";

interface PostCardActionsProps {
    postId: string;
    likesCount: number;
    likedByUser: boolean;
    savedByUser: boolean;
    commentsCount: number;
    commentedByUser: boolean;
    refetch: (
        options?: RefetchOptions
    ) => Promise<QueryObserverResult<InfiniteData<PostPage, unknown>, Error>>;
}

function PostCardActions({
    postId,
    likesCount,
    likedByUser,
    savedByUser,
    commentsCount,
    commentedByUser,
    refetch,
}: PostCardActionsProps): React.ReactNode {
    return (
        <div className="flex justify-between">
            <div className="flex gap-2">
                <div className="flex justify-center items-center gap-1">
                    <LikeButton
                        postId={postId}
                        likesCount={likesCount}
                        likedByUser={likedByUser}
                        refetch={refetch}
                    />
                </div>
                <div className="flex justify-center items-center gap-1">
                    <CommentsButton
                        postId={postId}
                        commentsCount={commentsCount}
                        commentedByUser={commentedByUser}
                        refetchPosts={refetch}
                    />
                </div>
            </div>
            <div className="flex gap-2">
                <SaveButton
                    postId={postId}
                    savedByUser={savedByUser}
                />
            </div>
        </div>
    );
}
export default PostCardActions;
