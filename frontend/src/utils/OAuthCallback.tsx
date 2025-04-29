import { JSX, useEffect } from "react";
import { useNavigate } from "react-router";
import { authGoogleCallback } from "../services/auth-service";
import { useAuthStore } from "../stores/auth-store";

function clearQueryParams(): void {
    const url = new URL(window.location.href);
    url.search = "";
    window.history.replaceState({}, document.title, url.toString());
}

function OAuthCallback(): JSX.Element {
    const { isAuthenticated, setIsAuthenticated } = useAuthStore();

    const navigate = useNavigate();

    useEffect(() => {
        async function handleOAuthCallback(): Promise<void> {
            try {
                const query = window.location.search;
                await authGoogleCallback(query);
                clearQueryParams();
                setIsAuthenticated(true);
            } finally {
                if (isAuthenticated) {
                    navigate("/canvas");
                } else {
                    navigate("/auth/login");
                }
            }
        }
        handleOAuthCallback();
    }, [isAuthenticated, navigate, setIsAuthenticated]);

    return (
        <div
            className="flex justify-center items-center bg-base-200"
            style={{
                height: `calc(100vh - ${NAVBAR_HEIGHT})`,
            }}
        >
            <span className="loading loading-ring loading-xl"></span>
        </div>
    );
}

export default OAuthCallback;
