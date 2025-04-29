import { useEffect } from "react";
import { Route, Routes, useLocation, useNavigate } from "react-router";
import Layout from "./layouts/Layout";
import CanvasPage from "./pages/CanvasPage";
import LandingPage from "./pages/LandingPage";
import LogInPage from "./pages/LogInPage";
import NotFoundPage from "./pages/NotFoundPage";
import SignUpPage from "./pages/SignUpPage";
import { isUserLoggedIn } from "./services/auth-service";
import { useAuthStore } from "./stores/auth-store";
import AuthenticatedRoute from "./utils/AuthenticatedRoute";
import OAuthCallback from "./utils/OAuthCallback";
import UnauthenticatedRoute from "./utils/UnauthenticatedRoute";

function clearQueryParams(): void {
    const url = new URL(window.location.href);
    url.search = "";
    window.history.replaceState({}, document.title, url.toString());
}

function App(): React.ReactNode {
    const location = useLocation();
    const navigate = useNavigate();
    const setIsAuthenticated = useAuthStore(
        (state) => state.setIsAuthenticated
    );

    // Check if the user is logged in when the app loads
    useEffect(() => {
        async function initAuth(): Promise<void> {
            const isLoggedIn = await isUserLoggedIn();
            setIsAuthenticated(isLoggedIn);
        }
        initAuth();
    }, [setIsAuthenticated]);

    const urlParams = new URLSearchParams(window.location.search);
    const isGoogleOauthCallback =
        urlParams.has("state") && urlParams.has("code");

    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route
                    index
                    element={
                        <UnauthenticatedRoute redirectTo="/canvas">
                            {isGoogleOauthCallback ? (
                                <OAuthCallback />
                            ) : (
                                <LandingPage />
                            )}
                        </UnauthenticatedRoute>
                    }
                />
                <Route
                    path="canvas"
                    element={
                        <AuthenticatedRoute redirectTo="/">
                            <CanvasPage />
                        </AuthenticatedRoute>
                    }
                />
            </Route>
            <Route path="auth">
                <Route
                    path="login"
                    element={
                        <UnauthenticatedRoute redirectTo="/canvas">
                            <LogInPage />
                        </UnauthenticatedRoute>
                    }
                />
                <Route
                    path="signup"
                    element={
                        <UnauthenticatedRoute redirectTo="/canvas">
                            <SignUpPage />
                        </UnauthenticatedRoute>
                    }
                />
            </Route>
            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    );
}

export default App;
