import React from "react";
import PostsGrid from "../../components/PostsGrid";
import { fetchPosts } from "../../services/posts-service";
import { useAuthStore } from "../../stores/auth-store";

function AccountPostsPage(): React.ReactNode {
    const { userId } = useAuthStore();

    const headerContent = (
        <header className="flex items-center justify-center p-8">
            <h1 className="text-2xl font-bold">My Pixelarts</h1>
        </header>
    );

    return (
        <PostsGrid
            queryKey={userId ? ["posts", userId] : ["posts"]}
            queryFn={({ pageParam }) => fetchPosts({ pageParam, userId })}
            header={headerContent}
        />
    );
}

export default AccountPostsPage;
