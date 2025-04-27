import { JSX, useEffect } from "react";
import { useNavigate } from "react-router";
import { authGoogleCallback } from "../services/auth-service";
import { useAuthStore } from "../stores/auth-store";

function OAuthCallback(): JSX.Element {
    const { isAuthenticated, setIsAuthenticated } = useAuthStore();

    const navigate = useNavigate();

    useEffect(() => {
        async function handleOAuthCallback(): Promise<void> {
            try {
                await authGoogleCallback(window.location.search);
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

    return <></>;
}

export default OAuthCallback;
