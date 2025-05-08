import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { FaRegPaperPlane } from "react-icons/fa";
import { postComment } from "../../services/posts-service";

type CommentFormValues = {
    comment: string;
};

type SendCommentFormProps = {
    postId: string;
    onCommentSent?: () => void;
};

function SendCommentForm({
    postId,
    onCommentSent,
}: SendCommentFormProps): React.ReactNode {
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<CommentFormValues>({
        defaultValues: { comment: "" },
    });

    const sendCommentMutation = useMutation({
        mutationFn: (text: string) => postComment(postId, text),
        onSuccess: () => {
            reset();
            if (onCommentSent) {
                onCommentSent();
            }
        },
    });

    function onSubmit(data: CommentFormValues): void {
        const trimmed = data.comment.trim();
        sendCommentMutation.mutate(trimmed);
    }

    return (
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
                        message: "Comment must be under 1000 characters",
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
    );
}

export default SendCommentForm;
