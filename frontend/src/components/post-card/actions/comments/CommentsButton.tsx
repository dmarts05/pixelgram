import { useInfiniteQuery } from "@tanstack/react-query";
import React, { useState } from "react";
import { FaRegComment } from "react-icons/fa";
import { fetchPostComments } from "../../../../services/posts-service";
import CommentsModal from "./CommentsModal";

type CommentsButtonProps = {
    postId: string;
};

function CommentsButton({ postId }: CommentsButtonProps): React.ReactNode {
    const modalId = `comments-modal-${postId}`;
    const [isModalOpen, setIsModalOpen] = useState(false);

    const {
        data,
        error,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        status,
        refetch,
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
        const modal = document.getElementById(modalId) as HTMLDialogElement;
        modal.showModal();
    }

    function handleCloseModal(): void {
        setIsModalOpen(false);
    }

    return (
        <>
            <button
                onClick={handleOpenModal}
                className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
            >
                <FaRegComment />
            </button>

            <CommentsModal
                postId={postId}
                modalId={modalId}
                status={status}
                error={error}
                data={data!}
                hasNextPage={hasNextPage}
                isFetchingNextPage={isFetchingNextPage}
                fetchNextPage={fetchNextPage}
                refetch={refetch}
                onClose={handleCloseModal}
            />
        </>
    );
}

export default CommentsButton;
