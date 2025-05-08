import {
    InfiniteData,
    QueryObserverResult,
    RefetchOptions,
} from "@tanstack/react-query";
import { FaRegBookmark } from "react-icons/fa";
import { PostPage } from "../../PostsGrid";
import CommentsButton from "./CommentsButton";
import LikeButton from "./LikeButton";

interface PostCardActionsProps {
    postId: string;
    likesCount: number;
    likedByUser: boolean;
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
                <button
                    onClick={() => console.log("Bookmark")}
                    className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
                >
                    <FaRegBookmark />
                </button>
            </div>
        </div>
    );
}
export default PostCardActions;
