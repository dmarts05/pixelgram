import { useInfiniteQuery } from "@tanstack/react-query";
import React from "react";
import { Post } from "../types/post";
import FullPageErrorAlert from "./FullPageErrorAlert";
import FullPageSpinner from "./FullPageSpinner";
import InfiniteScrollIntersectionObserver from "./InfiniteScrollIntersectionObserver";
import PostCard from "./post-card/PostCard";

type PostPage = {
    data: Post[];
    nextPage: number | null;
};

interface PostsGridProps {
    queryKey: string[];
    queryFn: (params: { pageParam: number }) => Promise<PostPage>;
    header?: React.ReactNode;
}

function PostsGrid({
    queryKey,
    queryFn,
    header,
}: PostsGridProps): React.ReactNode {
    const {
        data,
        error,
        fetchNextPage,
        hasNextPage,
        isFetchingNextPage,
        status,
    } = useInfiniteQuery({
        queryKey,
        queryFn,
        initialPageParam: 1,
        getNextPageParam: (lastPage) => lastPage.nextPage,
        refetchInterval: 60000, // Refetch every minute
    });

    switch (status) {
        case "pending":
            return <FullPageSpinner />;
        case "error":
            return <FullPageErrorAlert errorMessage={String(error)} />;
    }

    return (
        <>
            {header}
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

export default PostsGrid;
