import { JSX, useEffect } from "react";
import { useNavigate } from "react-router";
import { authGoogleCallback } from "../services/auth-service";
import { useAuthStore } from "../stores/auth-store";

function getQueryFromHash(): string {
    const hash = window.location.hash;
    const queryStart = hash.indexOf("?");
    return queryStart !== -1 ? hash.slice(queryStart) : "";
}

function OAuthCallback(): JSX.Element {
    const { isAuthenticated, setIsAuthenticated } = useAuthStore();

    const navigate = useNavigate();

    useEffect(() => {
        async function handleOAuthCallback(): Promise<void> {
            try {
                await authGoogleCallback(getQueryFromHash());
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
