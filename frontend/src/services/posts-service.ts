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

export async function deletePost(postId: string): Promise<void> {
    const res = await fetchApi(`posts/${postId}`, {
        method: "DELETE",
    });
    if (!res.ok) {
        throw new Error("Failed to delete post");
    }
}

export async function autogenerateCaption(imageUrl: string): Promise<string> {
    
    try {
        // Convert dataURL to Blob
        const response = await fetch(imageUrl);
        const blob = await response.blob();

        // Create FormData and add blob
        const formData = new FormData();
        formData.append("file", blob, "image.png");

        // Send as multipart/form-data
        const apiResponse = await fetchApi('captions', {
            method: "POST",
            body: formData,
        });

        if(!apiResponse.ok) {
            const errorData = await apiResponse.json();
            throw new Error(
                `Error while fetching the caption: ${errorData.detail || apiResponse.statusText}`
            );
        }
        const data = await apiResponse.json();
        return data.caption;

    } catch(error: unknown) {
        console.error("Error:", error);
        let errorMessage = "An unknown error occurred";

        if (error instanceof Error) {
            errorMessage = error.message;
        }

        throw new Error(errorMessage);
    }   
}

export async function publishPost(imageUrl:string, description:string):Promise<void> {
    try {
        // Convert dataURL to Blob
        const response = await fetch(imageUrl);
        const blob = await response.blob();

        // Create FormData and add blob and description
        const formData = new FormData();
        formData.append("file", blob, "image.png");
        formData.append("description", description);

        const apiResponse = await fetchApi("posts", {
            method: "POST",
            body: formData,
        });

        if (!apiResponse.ok) {
            const errorData = await apiResponse.json();
            throw new Error(
                `Error while publishing the pixelart: ${errorData.detail || apiResponse.statusText}`
            );
        }
    } catch (error: unknown) {
        console.error("Error publishing pixelart:", error);
        let errorMessage = "An unknown error occurred";

        if (error instanceof Error) {
            errorMessage = error.message;
        }

        throw new Error(errorMessage);
    }
}
