import { useAuthStore } from "../stores/auth-store";

export async function fetchApi(
    url: string,
    options: RequestInit = {}
): Promise<Response> {
    const response = await fetch(url, {
        ...options,
        credentials: "include",
        signal: AbortSignal.timeout(10000), // 10 seconds timeout
    });

    // If the response is 401 (Unauthorized), set user as not authenticated
    if (response.status === 401) {
        const setIsAuthenticated = useAuthStore.getState().setIsAuthenticated;
        setIsAuthenticated(false);
    }

    return response;
}
