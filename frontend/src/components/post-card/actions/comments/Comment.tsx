import { useMutation } from "@tanstack/react-query";
import { useEffect, useRef, useState } from "react";
import { FaRegTrashAlt } from "react-icons/fa";
import { deleteComment } from "../../../../services/posts-service";
import PostCardTimestamp from "../../PostCardTimestamp";
import ConfirmDeleteCommentModal from "./ConfirmDeleteCommentModal";

interface CommentProps {
    postId: string;
    commentId: string;
    authorUsername: string;
    content: string;
    createdAt: Date;
    byUser: boolean;
    refetchPosts: () => void;
    refetchComments: () => void;
}

function Comment({
    postId,
    commentId,
    authorUsername,
    content,
    createdAt,
    byUser,
    refetchPosts,
    refetchComments,
}: CommentProps): React.ReactNode {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isClamped, setIsClamped] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const bubbleRef = useRef<HTMLDivElement | null>(null);

    const deleteCommentMutation = useMutation({
        mutationFn: () => deleteComment(postId, commentId),
        onSuccess: () => {
            refetchPosts();
            refetchComments();
            setIsModalOpen(false);
        },
        onError: () => {
            setIsModalOpen(false);
            // Optionally show error UI
        },
    });

    // Check if the bubble overflows when clamped.
    useEffect(() => {
        const el = bubbleRef.current;
        if (!el) {
            return;
        }

        // When not expanded, the bubble is clamped and we compare its scrollHeight with clientHeight.
        // This determines if there's hidden overflow content.
        const clamped = el.scrollHeight > el.clientHeight;
        setIsClamped(clamped);
    }, [content]);

    return (
        <div className="flex flex-col">
            <div className={`chat ${byUser ? "chat-end" : "chat-start"}`}>
                <div className="chat-header mb-1.5">
                    <div className="flex items-center gap-2">
                        <strong className="font-semibold">
                            {authorUsername}
                        </strong>
                        <div className="flex items-center gap-1">
                            <PostCardTimestamp
                                createdAt={createdAt}
                                color="text-content text-right"
                                uppercase={false}
                            />
                            {byUser && (
                                <button
                                    className="text-xs hover:text-error transition-colors cursor-pointer"
                                    onClick={() => setIsModalOpen(true)}
                                    disabled={deleteCommentMutation.isPending}
                                    aria-label="Delete comment"
                                >
                                    <FaRegTrashAlt />
                                </button>
                            )}
                        </div>
                    </div>
                </div>
                <div
                    className={`chat-bubble max-w-xs text-sm whitespace-pre-wrap break-words p-1 px-3 ${
                        isExpanded ? "" : "line-clamp-3"
                    } ${byUser && "chat-bubble-primary"}`}
                    ref={bubbleRef}
                >
                    <p>{content}</p>
                </div>
            </div>
            {isClamped && (
                <div className={`chat-footer flex ${byUser && "justify-end"}`}>
                    <button
                        onClick={() => setIsExpanded((prev) => !prev)}
                        className={`text-xs font-medium hover:underline cursor-pointer ${
                            byUser
                                ? "text-primary mr-3"
                                : "text-base-content ml-3"
                        }`}
                    >
                        {isExpanded ? "Show less" : "Show more"}
                    </button>
                </div>
            )}
            <ConfirmDeleteCommentModal
                isOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)}
                onConfirm={() => deleteCommentMutation.mutate()}
                isLoading={deleteCommentMutation.isPending}
                commentId={commentId}
            />
            {deleteCommentMutation.isError && (
                <span className="text-sm font-semibold text-error">Failed to delete comment. Please try again later.</span>
            )}
        </div>
    );
}

export default Comment;
