import React from 'react';
import PostsGrid from "../../components/PostsGrid";
import { fetchSavedPosts } from "../../services/posts-service";
import { useAuthStore } from '../../stores/auth-store';

function SavedPostsPage(): React.ReactNode {

    const userId = useAuthStore((state) => state.userId);

    const headerContent = (
        <header className="flex items-center justify-center pt-8">
            <h1 className="text-2xl font-bold">Saved posts</h1>
        </header>
    );
    

    return (
        <PostsGrid
            queryKey={userId ? ["savedPosts", userId] : ["savedPosts"]}
            queryFn={({pageParam }) => fetchSavedPosts({pageParam, userId})}
            header ={headerContent}
            
            />
    );
}

export default SavedPostsPage;