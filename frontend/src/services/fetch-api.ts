import { useAuthStore } from "../stores/auth-store";

export async function fetchApi(
    url: string,
    options: RequestInit = {}
): Promise<Response> {
    const response = await fetch(url, {
        ...options,
        credentials: "include",
    });

    // If the response is 401 (Unauthorized), set user as not authenticated
    if (response.status === 401) {
        const setIsAuthenticated = useAuthStore.getState().setIsAuthenticated;
        setIsAuthenticated(false);
    }

    return response;
}
