import { useEffect, useRef, useState } from "react";

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
        const clamped = pElement.scrollHeight > pElement.clientHeight;
        setIsClamped(clamped);
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

export default PostCardDescription;
