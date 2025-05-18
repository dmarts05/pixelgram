import { InfiniteData } from "@tanstack/react-query";
import React from "react";
import { FetchPostCommentsResponse } from "../../../../services/posts-service";
import SendCommentForm from "../../../forms/SendCommentForm";
import FullPageErrorAlert from "../../../FullPageErrorAlert";
import FullPageSpinner from "../../../FullPageSpinner";
import BaseModal from "../../../BaseModal";
import CommentsBubbles from "./CommentsBubbles";

type CommentsModalProps = {
    postId: string;
    isOpen: boolean;
    status: string;
    error: unknown;
    data: InfiniteData<FetchPostCommentsResponse>;
    hasNextPage: boolean;
    isFetchingNextPage: boolean;
    fetchNextPage: () => void;
    refetchPosts: () => void;
    refetchComments: () => void;
    onClose: () => void;
};

function CommentsModal({
    postId,
    isOpen,
    status,
    error,
    data,
    hasNextPage,
    isFetchingNextPage,
    fetchNextPage,
    refetchPosts,
    refetchComments,
    onClose,
}: CommentsModalProps): React.ReactNode {
    let modalContent: React.ReactNode = null;
    switch (status) {
        case "pending":
            modalContent = <FullPageSpinner />;
            break;
        case "error":
            modalContent = <FullPageErrorAlert errorMessage={String(error)} />;
            break;
        case "success": {
            const comments = data.pages.flatMap((page) => page.data);
            modalContent = (
                <>
                    <CommentsBubbles
                        comments={comments}
                        hasNextPage={hasNextPage}
                        isFetchingNextPage={isFetchingNextPage}
                        fetchNextPage={fetchNextPage}
                        refetchPosts={refetchPosts}
                        refetchComments={refetchComments}
                    />
                    <SendCommentForm
                        postId={postId}
                        onCommentSent={() => {
                            refetchPosts();
                            refetchComments();
                        }}
                    />
                </>
            );
            break;
        }
    }

    return (
        <BaseModal
            isOpen={isOpen}
            onClose={onClose}
            ariaLabel="Comments dialog"
        >
            <h3 className="font-bold text-lg">Comments</h3>
            <div>{modalContent}</div>
        </BaseModal>
    );
}

export default CommentsModal;
