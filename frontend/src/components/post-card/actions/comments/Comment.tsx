import { useEffect, useRef, useState } from "react";
import PostCardTimestamp from "../../PostCardTimestamp";

type CommentProps = {
    authorUsername: string;
    content: string;
    createdAt: Date;
    byUser: boolean;
};

function Comment({
    authorUsername,
    content,
    createdAt,
    byUser,
}: CommentProps): React.ReactNode {
    const [isExpanded, setIsExpanded] = useState(false);
    const [isClamped, setIsClamped] = useState(false);
    const bubbleRef = useRef<HTMLDivElement | null>(null);

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
                <div
                    className={`chat-bubble max-w-xs text-sm whitespace-pre-wrap break-words p-1 px-3 ${
                        isExpanded ? "" : "line-clamp-3"
                    } ${byUser && "chat-bubble-primary"}`}
                    ref={bubbleRef}
                >
                    <div className="flex justify-between items-center gap-2">
                        <strong className="font-semibold">
                            {authorUsername}
                        </strong>
                        <PostCardTimestamp
                            createdAt={createdAt}
                            color="text-content text-right"
                            uppercase={false}
                        />
                    </div>
                    <p>{content}</p>
                </div>
            </div>
            {isClamped && (
                <button
                    onClick={() => setIsExpanded((prev) => !prev)}
                    className={`text-xs font-medium hover:underline cursor-pointer ${
                        byUser
                            ? "text-primary self-end mr-3"
                            : "text-base-content self-start ml-3"
                    }`}
                >
                    {isExpanded ? "Show less" : "Show more"}
                </button>
            )}
        </div>
    );
}

export default Comment;
