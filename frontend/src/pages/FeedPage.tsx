import { useInfiniteQuery } from "@tanstack/react-query";
import React, { useEffect, useRef } from "react";
import { MdErrorOutline, MdInfoOutline } from "react-icons/md";
import PostCard from "../components/post-card/PostCard";
import { fetchPosts } from "../services/posts-service";
import { Post } from "../types/post";
import { NAVBAR_HEIGHT } from "../utils/constants";

function FeedPage(): React.ReactNode {
    const {
        data,
        error,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        status,
    } = useInfiniteQuery({
        queryKey: ["posts"],
        queryFn: fetchPosts,
        initialPageParam: 1,
        getNextPageParam: (lastPage) => lastPage.nextPage,
        refetchInterval: 60000, // Refetch every minute
    });

    const sentinelRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                const [entry] = entries;
                // When the sentinel becomes visible and there is a next page, fetch it
                if (
                    entry.isIntersecting &&
                    hasNextPage &&
                    !isFetchingNextPage
                ) {
                    fetchNextPage();
                }
            },
            { threshold: 1.0 }
        );

        const currentSentinel = sentinelRef.current;
        if (currentSentinel) {
            observer.observe(currentSentinel);
        }

        // Cleanup the observer on component unmount or when ref changes
        return (): void => {
            if (currentSentinel) {
                observer.unobserve(currentSentinel);
            }
        };
    }, [fetchNextPage, hasNextPage, isFetchingNextPage]);

    switch (status) {
        case "pending":
            return (
                <div
                    className="flex justify-center items-center"
                    style={{
                        height: `calc(100vh - ${NAVBAR_HEIGHT})`,
                    }}
                >
                    <span className="loading loading-ring loading-xl"></span>
                </div>
            );
        case "error":
            return (
                <div
                    className="flex justify-center items-center"
                    style={{
                        height: `calc(100vh - ${NAVBAR_HEIGHT})`,
                    }}
                >
                    <div
                        role="alert"
                        className="alert alert-error alert-soft !shadow-md w-80"
                    >
                        <MdErrorOutline className="text-xl" />
                        <span>{String(error)}</span>
                    </div>
                </div>
            );
        case "success":
            break;
    }

    return (
        <>
            <main className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-8 p-8">
                {data?.pages.map((page, pageIndex) => (
                    <React.Fragment key={pageIndex}>
                        {page.data.map((post: Post) => (
                            <React.Fragment key={post.id}>
                                <PostCard post={post} />
                            </React.Fragment>
                        ))}
                    </React.Fragment>
                ))}
            </main>

            {/* Sentinel element to trigger loading more posts */}
            <div
                ref={sentinelRef}
                className="flex justify-center items-center pb-8 px-8"
            >
                {isFetchingNextPage ? (
                    <span className="loading loading-ring loading-md"></span>
                ) : (
                    !hasNextPage && (
                        <div
                            role="alert"
                            className="alert alert-info alert-soft !shadow-md w-80"
                        >
                            <MdInfoOutline className="text-xl" />
                            <span>No more posts to load.</span>
                        </div>
                    )
                )}
            </div>
        </>
    );
}

export default FeedPage;
