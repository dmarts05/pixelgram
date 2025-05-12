import { useState } from "react";
import { FaRegTrashAlt } from "react-icons/fa";
import {
    useMutation,
    InfiniteData,
    QueryObserverResult,
    RefetchOptions,
} from "@tanstack/react-query";
import { deletePost } from "../../../services/posts-service";
import { PostPage } from "../../PostsGrid";
import ConfirmDeleteModal from "./delete/ConfirmDeleteModal";

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
                className="rounded-full text-lg hover:text-error transition-colors cursor-pointer"
            >
                <FaRegTrashAlt />
            </button>
            <ConfirmDeleteModal
                isOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)}
                onConfirm={() => mutation.mutate()}
                isLoading={mutation.isPending}
            />
            {mutation.isError && (
                <span className="text-sm font-semibold text-error">Error</span>
            )}
        </>
    );
}

export default DeleteButton;
