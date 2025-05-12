import { useAuthStore } from "../stores/auth-store";
import { API_URL } from "../utils/constants";

export async function fetchApi(
    url: string,
    options: RequestInit = {}
): Promise<Response> {
    const fullUrl = `${API_URL}/${url}`;
    const response = await fetch(fullUrl, {
        ...options,
        credentials: "include",
        signal: AbortSignal.timeout(15000), // 15 seconds timeout
    });

    // If the response is 401 (Unauthorized), set user as not authenticated
    if (response.status === 401) {
        const setUserId = useAuthStore.getState().setUserId;
        setUserId(null);
    }

    return response;
}
