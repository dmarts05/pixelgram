import React from "react";
import PostsGrid from "../components/PostsGrid";
import { fetchPosts } from "../services/posts-service";

function FeedPage(): React.ReactNode {
    return <PostsGrid queryKey={["posts"]} queryFn={fetchPosts} />;
}

export default FeedPage;
