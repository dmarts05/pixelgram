import { useState } from "react";
import { FaRegTrashAlt } from "react-icons/fa";
import {
    useMutation,
    InfiniteData,
    QueryObserverResult,
    RefetchOptions,
} from "@tanstack/react-query";
import { deletePost } from "../../../../services/posts-service";
import { PostPage } from "../../../PostsGrid";
import ConfirmDeleteModal from "./ConfirmDeletePostModal";

interface DeleteButtonProps {
    postId: string;
    refetch: (
        options?: RefetchOptions
    ) => Promise<QueryObserverResult<InfiniteData<PostPage, unknown>, Error>>;
}

function DeleteButton({ postId, refetch }: DeleteButtonProps): React.ReactNode {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const mutation = useMutation({
        mutationFn: async () => {
            await deletePost(postId);
        },
        onSuccess: () => {
            refetch();
            setIsModalOpen(false);
        },
    });

    return (
        <>
            <button
                onClick={() => setIsModalOpen(true)}
                className="text-lg hover:text-error transition-colors cursor-pointer"
                aria-haspopup="dialog"
                aria-expanded={isModalOpen}
            >
                <FaRegTrashAlt />
            </button>
            <ConfirmDeleteModal
                isOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)}
                onConfirm={() => mutation.mutate()}
                isLoading={mutation.isPending}
                postId={postId}
            />
            {mutation.isError && (
                <span className="text-sm font-semibold text-error">Error</span>
            )}
        </>
    );
}

export default DeleteButton;
