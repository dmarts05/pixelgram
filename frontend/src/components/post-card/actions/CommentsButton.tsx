import { useInfiniteQuery, useMutation } from "@tanstack/react-query";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { FaRegComment, FaRegPaperPlane } from "react-icons/fa";
import {
    fetchPostComments,
    postComment,
} from "../../../services/posts-service";
import FullPageErrorAlert from "../../FullPageErrorAlert";
import FullPageSpinner from "../../FullPageSpinner";
import InfiniteScrollIntersectionObserver from "../../InfiniteScrollIntersectionObserver";
import Modal from "../../Modal";
import PostCardComment from "../PostCardComment";

type CommentFormValues = {
    comment: string;
};

type CommentsButtonProps = {
    postId: string;
};

function CommentsButton({ postId }: CommentsButtonProps): React.ReactNode {
    const modalId = `comments-modal-${postId}`;
    const [isModalOpen, setIsModalOpen] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<CommentFormValues>({
        defaultValues: { comment: "" },
    });

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
        refetchInterval: 60000,
        enabled: isModalOpen,
    });

    function handleOpenModal(): void {
        setIsModalOpen(true);
        const modal = document.getElementById(modalId) as HTMLDialogElement;
        modal.showModal();
    }

    function handleCloseModal(): void {
        setIsModalOpen(false);
    }

    const sendCommentMutation = useMutation({
        mutationFn: (text: string) => postComment(postId, text),
        onSuccess: () => {
            reset();
            refetch();
        },
    });

    function onSubmit(data: CommentFormValues): void {
        const trimmed = data.comment.trim();
        sendCommentMutation.mutate(trimmed);
    }

    let modalContent: React.ReactNode = null;
    switch (status) {
        case "pending":
            modalContent = <FullPageSpinner />;
            break;
        case "error":
            modalContent = <FullPageErrorAlert errorMessage={String(error)} />;
            break;
        case "success":
            modalContent = (
                <div className="flex flex-col gap-4">
                    <div className="flex-grow h-[60vh] overflow-y-auto pb-1">
                        {data.pages.map((page, pageIndex) => (
                            <React.Fragment key={pageIndex}>
                                {page.data.map((comment) => (
                                    <React.Fragment key={comment.id}>
                                        <PostCardComment
                                            authorUsername={
                                                comment.authorUsername
                                            }
                                            content={comment.content}
                                            createdAt={comment.createdAt}
                                            byUser={comment.byUser}
                                        />
                                    </React.Fragment>
                                ))}
                            </React.Fragment>
                        ))}
                        <InfiniteScrollIntersectionObserver
                            onIntersect={(): void => {
                                if (hasNextPage) fetchNextPage();
                            }}
                            hasNextPage={hasNextPage}
                            isFetchingNextPage={isFetchingNextPage}
                            className="flex justify-center items-center pt-4"
                            noMoreItemsMessage="No more comments to load."
                        />
                    </div>
                    <form
                        onSubmit={handleSubmit(onSubmit)}
                        className="flex flex-col gap-2 pt-4 border-t-1 border-base-300"
                    >
                        <textarea
                            className="textarea w-full resize-none focus:outline-none"
                            rows={3}
                            placeholder="Write your comment..."
                            maxLength={1000}
                            {...register("comment", {
                                required: "Comment is required",
                                maxLength: {
                                    value: 1000,
                                    message:
                                        "Comment must be under 1000 characters",
                                },
                                validate: (value) => {
                                    const trimmed = value.trim();
                                    if (trimmed.length === 0) {
                                        return "Comment cannot be empty";
                                    }
                                    return true;
                                },
                            })}
                        />
                        {errors.comment && (
                            <span className="text-error text-sm">
                                {errors.comment.message}
                            </span>
                        )}
                        <div className="flex justify-end items-center">
                            <button
                                type="submit"
                                className="btn btn-sm btn-primary"
                                disabled={sendCommentMutation.isPending}
                            >
                                <FaRegPaperPlane />
                                Send
                            </button>
                        </div>
                    </form>
                </div>
            );
            break;
    }

    return (
        <>
            <button
                onClick={handleOpenModal}
                className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
            >
                <FaRegComment />
            </button>

            <Modal id={modalId} responsive={false} onClose={handleCloseModal}>
                {modalContent}
            </Modal>
        </>
    );
}

export default CommentsButton;
