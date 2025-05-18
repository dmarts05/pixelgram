import { useInfiniteQuery } from "@tanstack/react-query";
import React, { useState } from "react";
import { FaComment, FaRegComment } from "react-icons/fa";
import { fetchPostComments } from "../../../services/posts-service";
import CommentsModal from "./comments/CommentsModal";

type CommentsButtonProps = {
    postId: string;
    commentsCount: number;
    commentedByUser: boolean;
    refetchPosts: () => void;
};

function CommentsButton({
    postId,
    commentsCount,
    commentedByUser,
    refetchPosts,
}: CommentsButtonProps): React.ReactNode {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const {
        data,
        error,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        status,
        refetch: refetchComments,
    } = useInfiniteQuery({
        queryKey: ["comments", postId],
        queryFn: ({ pageParam }) => fetchPostComments(postId, pageParam),
        initialPageParam: 1,
        getNextPageParam: (lastPage) => lastPage.nextPage,
        refetchInterval: 60000, // Refetch every minute
        enabled: isModalOpen, // Only fetch when the modal is open
    });

    function handleOpenModal(): void {
        setIsModalOpen(true);
    }

    function handleCloseModal(): void {
        setIsModalOpen(false);
    }

    return (
        <>
            <button
                onClick={handleOpenModal}
                className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
                aria-haspopup="dialog"
                aria-expanded={isModalOpen}
            >
                {commentedByUser ? <FaComment /> : <FaRegComment />}
            </button>

            <span className="text-sm font-semibold">{commentsCount}</span>

            <CommentsModal
                postId={postId}
                isOpen={isModalOpen}
                status={status}
                error={error}
                data={data!}
                hasNextPage={hasNextPage}
                isFetchingNextPage={isFetchingNextPage}
                fetchNextPage={fetchNextPage}
                refetchPosts={refetchPosts}
                refetchComments={refetchComments}
                onClose={handleCloseModal}
            />
        </>
    );
}

export default CommentsButton;
