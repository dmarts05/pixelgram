import {
    InfiniteData,
    QueryObserverResult,
    RefetchOptions,
    useMutation,
} from "@tanstack/react-query";
import { FaHeart, FaRegHeart } from "react-icons/fa";
import { likePost, unlikePost } from "../../../services/posts-service";
import { PostPage } from "../../PostsGrid";

interface LikeButtonProps {
    postId: string;
    likesCount: number;
    likedByUser: boolean;
    refetch: (
        options?: RefetchOptions
    ) => Promise<QueryObserverResult<InfiniteData<PostPage, unknown>, Error>>;
}

function LikeButton({
    postId,
    likesCount,
    likedByUser,
    refetch,
}: LikeButtonProps): React.ReactNode {
    const likeUnlikeMutation = useMutation({
        mutationFn: async () => {
            if (!likedByUser) {
                await likePost(postId);
            } else {
                await unlikePost(postId);
            }
        },
        onSuccess: () => refetch(),
    });

    let likeCountElement: React.ReactNode = null;
    if (likeUnlikeMutation.isPending) {
        likeCountElement = (
            <span className="loading loading-ring loading-xs"></span>
        );
    } else if (likeUnlikeMutation.isError) {
        likeCountElement = <span className="text-sm font-semibold">-</span>;
    } else {
        likeCountElement = (
            <span className="text-sm font-semibold">{likesCount}</span>
        );
    }

    return (
        <>
            <button
                onClick={() => likeUnlikeMutation.mutate()}
                className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
            >
                {likedByUser ? <FaHeart /> : <FaRegHeart />}
            </button>
            {likeCountElement}
        </>
    );
}

export default LikeButton;
