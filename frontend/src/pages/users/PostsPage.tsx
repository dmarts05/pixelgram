import React from "react";
import PostsGrid from "../../components/PostsGrid";
import { fetchPosts } from "../../services/posts-service";
import { useAuthStore } from "../../stores/auth-store";
import { useParams, Navigate } from "react-router";
import { useQuery } from "@tanstack/react-query";
import { getUsernameById } from "../../services/account-service";

function UserPostsPage(): React.ReactNode {
    const { userId: authorId } = useParams<{ userId: string }>();
    const userId = useAuthStore((state) => state.userId);

    const { data, isLoading, isError } = useQuery({
        queryKey: ["user", authorId],
        queryFn: () => getUsernameById(authorId!),
    });

    if (authorId === userId) {
        console.log("User is trying to access their own posts");
        return <Navigate to="/account/posts" />;
    }

    const headerContent = (
        <header className="flex items-center justify-center pt-8">
            <h1 className="text-2xl font-bold">
                {isLoading ? (
                    <span className="loading loading-ring loading-md"></span>
                ) : isError ? (
                    <span className="loading loading-ring loading-md error"></span>
                ) : (
                    data?.username
                )}
                {"'s posts"}
            </h1>
        </header>
    );

    return (
        <PostsGrid
            queryKey={userId ? ["posts", userId] : ["posts"]}
            queryFn={({ pageParam }) =>
                fetchPosts({ pageParam, userId: authorId })
            }
            header={headerContent}
        />
    );
}

export default UserPostsPage;
