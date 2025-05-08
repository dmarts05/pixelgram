import { Post } from "../types/post";
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
