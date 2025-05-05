import { formatDistanceToNow } from "date-fns";
import { useEffect, useRef, useState } from "react";
import { FaRegBookmark, FaRegComment, FaRegHeart } from "react-icons/fa";
import { Post } from "../types/post";

type PostCardHeaderProps = {
    authorUsername: string;
};

function PostCardHeader({
    authorUsername,
}: PostCardHeaderProps): React.ReactNode {
    return (
        <div className="py-2 px-4">
            <span className="font-semibold text-sm">{authorUsername}</span>
        </div>
    );
}

type PostCardImageProps = {
    imageUrl: URL;
    imageAlt: string;
    height: number;
};

function PostCardImage({
    imageUrl,
    imageAlt,
    height,
}: PostCardImageProps): React.ReactNode {
    const dialogId = `image-modal-${imageUrl}`;

    function openModal(): void {
        const dialog = document.getElementById(dialogId) as HTMLDialogElement;
        dialog.showModal();
    }

    return (
        <>
            <figure onClick={openModal} className="cursor-pointer">
                <img
                    src={String(imageUrl)}
                    alt={imageAlt}
                    className="w-full border-y border-base-200"
                    height={height}
                />
            </figure>

            <dialog id={dialogId} className="modal">
                <div className="modal-box p-0">
                    <img
                        src={String(imageUrl)}
                        alt={imageAlt}
                        className="w-full"
                        height={height}
                    />
                </div>
                <form method="dialog" className="modal-backdrop">
                    <button>close</button>
                </form>
            </dialog>
        </>
    );
}

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

type PostCardDescriptionProps = {
    description: string;
};

function PostCardDescription({
    description,
}: PostCardDescriptionProps): React.ReactNode {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isClamped, setIsClamped] = useState(false);
    const pRef = useRef<HTMLParagraphElement | null>(null);

    // Check if the description overflows when clamped.
    useEffect(() => {
        const pElement = pRef.current;
        if (!pElement) {
            return;
        }

        // When not expanded, the paragraph is clamped and we compare its scrollHeight with clientHeight.
        // This determines if there's hidden overflow content.
        const isClamped = pElement.scrollHeight > pElement.clientHeight;
        setIsClamped(isClamped);
    }, []);

    return (
        <div>
            <p
                ref={pRef}
                className={`text-sm whitespace-normal break-words ${
                    isExpanded ? "" : "line-clamp-3"
                }`}
            >
                {description}
            </p>
            {isClamped && (
                <button
                    onClick={() => setIsExpanded((prev) => !prev)}
                    className="text-xs text-primary font-medium mt-1 hover:underline cursor-pointer"
                >
                    {isExpanded ? "Show less" : "Show more"}
                </button>
            )}
        </div>
    );
}

type PostCardTimestampProps = {
    createdAt: Date;
};

function PostCardTimestamp({
    createdAt,
}: PostCardTimestampProps): React.ReactNode {
    const timeAgo = formatDistanceToNow(new Date(createdAt), {
        addSuffix: true,
    });

    return <p className="text-xs text-base-content/60 uppercase">{timeAgo}</p>;
}

type PostCardProps = {
    post: Post;
};

function PostCard({ post }: PostCardProps): React.ReactNode {
    return (
        <article className="card bg-base-100 shadow-md">
            <PostCardHeader authorUsername={post.authorUsername} />
            <PostCardImage
                imageUrl={post.imageUrl}
                imageAlt={post.description}
                height={256}
            />
            <div className="card-body">
                <PostCardActions
                    onLike={() => console.log("Like")}
                    onComment={() => console.log("Comment")}
                    onBookmark={() => console.log("Bookmark")}
                />
                <PostCardDescription description={post.description} />
                <PostCardTimestamp createdAt={post.createdAt} />
            </div>
        </article>
    );
}

export default PostCard;
