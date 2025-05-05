import { Post } from "../types/post";
import { fetchApi } from "./fetch-api";

export type FetchPostsParams = {
    pageParam: number;
    pageSize?: number;
};

export type FetchPostsResponse = {
    data: Post[];
    nextPage: number | null;
    total: number;
};

export async function fetchPosts({
    pageParam,
    pageSize = 10,
}: FetchPostsParams): Promise<FetchPostsResponse> {
    const params = new URLSearchParams({
        page: String(pageParam),
        page_size: String(pageSize),
    });

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
