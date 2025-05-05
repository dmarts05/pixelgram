import React, { useEffect, useRef } from "react";
import { MdInfoOutline } from "react-icons/md";

type InfiniteScrollIntersectionObserverProps = {
    onIntersect: () => void;
    hasNextPage: boolean;
    isFetchingNextPage: boolean;
    className?: string;
    noMoreItemsMessage?: string;
    threshold?: number;
};

function InfiniteScrollIntersectionObserver({
    onIntersect,
    hasNextPage,
    isFetchingNextPage,
    className = "",
    noMoreItemsMessage = "No more items to load.",
    threshold = 1.0,
}: InfiniteScrollIntersectionObserverProps): React.ReactNode {
    const sentinelRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                const [entry] = entries;
                // Trigger onIntersect if the sentinel is fully in view, there are more items, and not currently fetching
                if (
                    entry.isIntersecting &&
                    hasNextPage &&
                    !isFetchingNextPage
                ) {
                    onIntersect();
                }
            },
            { threshold }
        );

        const currentSentinel = sentinelRef.current;
        if (currentSentinel) {
            observer.observe(currentSentinel);
        }

        // Cleanup the observer on component unmount or when dependencies change
        return (): void => {
            if (currentSentinel) {
                observer.unobserve(currentSentinel);
            }
        };
    }, [onIntersect, hasNextPage, isFetchingNextPage, threshold]);

    return (
        <div ref={sentinelRef} className={className}>
            {isFetchingNextPage ? (
                <span className="loading loading-ring loading-md"></span>
            ) : (
                !hasNextPage && (
                    <div
                        role="alert"
                        className="alert alert-info alert-soft !shadow-md w-80"
                    >
                        <MdInfoOutline className="text-xl" />
                        <span>{noMoreItemsMessage}</span>
                    </div>
                )
            )}
        </div>
    );
}

export default InfiniteScrollIntersectionObserver;
