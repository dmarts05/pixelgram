import { Post } from "../types/post";
import { PostComment } from "../types/post-comment";
import { fetchApi } from "./fetch-api";

export type FetchPostsParams = {
    pageParam: number;
    pageSize?: number;
    userId?: string | null;
};

export type FetchPostsResponse = {
    data: Post[];
    nextPage: number | null;
    total: number;
};

export async function fetchPosts({
    pageParam,
    pageSize = 10,
    userId = null,
}: FetchPostsParams): Promise<FetchPostsResponse> {
    const params = new URLSearchParams({
        page: String(pageParam),
        page_size: String(pageSize),
        user_id: userId || "",
    });

    if (userId) {
        params.append("user_id", userId);
    }

    const res = await fetchApi(`posts?${params}`, {
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("Failed to fetch posts");
    }

    return res.json();
}

export async function fetchSavedPosts({
    pageParam,
    pageSize = 10,
    userId = null,
}: FetchPostsParams): Promise<FetchPostsResponse> {
    const params = new URLSearchParams({
        page: String(pageParam),
        page_size: String(pageSize),
    });

    if (userId) {
        params.append("user_id", userId);
    }

    const res = await fetchApi(`posts/saved?${params}`, {
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("Failed to fetch posts");
    }

    return res.json();
}

export async function likePost(postId: string): Promise<void> {
    const res = await fetchApi(`posts/${postId}/like`, {
        method: "POST",
    });

    if (!res.ok) {
        throw new Error("Failed to like post");
    }
}

export async function unlikePost(postId: string): Promise<void> {
    const res = await fetchApi(`posts/${postId}/like`, {
        method: "DELETE",
    });

    if (!res.ok) {
        throw new Error("Failed to unlike post");
    }
}

export async function savePost(postId: string): Promise<void> {
    const res = await fetchApi(`posts/${postId}/save`, {
        method: "POST",
    });

    if (!res.ok) {
        throw new Error("Failed to save post");
    }
}
export async function unsavePost(postId: string): Promise<void> {
    const res = await fetchApi(`posts/${postId}/save`, {
        method: "DELETE",
    });
    if (!res.ok) {
        throw new Error("Failed to unsave post");
    }
}

export type FetchPostCommentsResponse = {
    data: PostComment[];
    nextPage: number | null;
    total: number;
};

export async function fetchPostComments(
    postId: string,
    pageParam: number,
    pageSize = 10
): Promise<FetchPostCommentsResponse> {
    const params = new URLSearchParams({
        page: String(pageParam),
        page_size: String(pageSize),
    });

    const res = await fetchApi(`posts/${postId}/comments?${params}`, {
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("Failed to fetch post comments");
    }

    return res.json();
}

export async function postComment(
    postId: string,
    commentText: string
): Promise<PostComment> {
    const res = await fetchApi(`posts/${postId}/comments`, {
        method: "POST",
        body: JSON.stringify({ content: commentText }),
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("Failed to post comment");
    }

    return res.json();
}

export async function deleteComment(
    postId: string,
    commentId: string
): Promise<void> {
    const res = await fetchApi(`posts/${postId}/comments/${commentId}`, {
        method: "DELETE",
    });

    if (!res.ok) {
        throw new Error("Failed to delete comment");
    }
}
