import { FaRegBookmark, FaRegComment, FaRegHeart } from "react-icons/fa";

type PostCardActionsProps = {
    onLike: () => void;
    onComment: () => void;
    onBookmark: () => void;
};

function PostCardActions({
    onLike,
    onComment,
    onBookmark,
}: PostCardActionsProps): React.ReactNode {
    return (
        <div className="flex justify-between">
            <div className="flex gap-2">
                <button
                    onClick={onLike}
                    className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
                >
                    <FaRegHeart />
                </button>
                <button
                    onClick={onComment}
                    className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
                >
                    <FaRegComment />
                </button>
            </div>
            <div className="flex gap-2">
                <button
                    onClick={onBookmark}
                    className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
                >
                    <FaRegBookmark />
                </button>
            </div>
        </div>
    );
}
export default PostCardActions;
