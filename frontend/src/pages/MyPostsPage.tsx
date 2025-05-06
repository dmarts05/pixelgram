import { useInfiniteQuery } from "@tanstack/react-query";
import React from "react";
import { MdErrorOutline } from "react-icons/md";
import InfiniteScrollIntersectionObserver from "../components/InfiniteScrollIntersectionObserver";
import PostCard from "../components/post-card/PostCard";
import { fetchPosts } from "../services/posts-service";
import { Post } from "../types/post";
import { NAVBAR_HEIGHT } from "../utils/constants";
import { useAuthStore } from "../stores/auth-store";

function MyPostsPage(): React.ReactNode {
    const { userId } = useAuthStore();
    const {
        data,
        error,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        status,
    } = useInfiniteQuery({
        queryKey: ["posts"],
        queryFn: ({ pageParam }) => fetchPosts({ pageParam, userId: userId }),
        initialPageParam: 1,
        getNextPageParam: (lastPage) => lastPage.nextPage,
        refetchInterval: 60000, // Refetch every minute
    });

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
            <main className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 p-8">
                {data.pages.map((page, pageIndex) => (
                    <React.Fragment key={pageIndex}>
                        {page.data.map((post: Post) => (
                            <React.Fragment key={post.id}>
                                <PostCard post={post} />
                            </React.Fragment>
                        ))}
                    </React.Fragment>
                ))}
            </main>

            <InfiniteScrollIntersectionObserver
                onIntersect={(): void => {
                    if (hasNextPage) {
                        fetchNextPage();
                    }
                }}
                hasNextPage={hasNextPage}
                isFetchingNextPage={isFetchingNextPage}
                className="flex justify-center items-center pb-8 px-8"
                noMoreItemsMessage="No more posts to load."
            />
        </>
    );
}

export default MyPostsPage;
