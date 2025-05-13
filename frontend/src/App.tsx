import { useEffect } from "react";
import { Route, Routes, useNavigate } from "react-router";
import AuthenticatedRoute from "./components/AuthenticatedRoute";
import UnauthenticatedRoute from "./components/UnauthenticatedRoute";
import Layout from "./layouts/Layout";
import AccountPostPage from "./pages/account/AccountPostsPage";
import SavedPostsPage from "./pages/account/SavedPostsPage";
import SettingsPage from "./pages/account/SettingsPage";
import CanvasPage from "./pages/CanvasPage";
import FeedPage from "./pages/FeedPage";
import LandingPage from "./pages/LandingPage";
import LogInPage from "./pages/LogInPage";
import NotFoundPage from "./pages/NotFoundPage";
import SignUpPage from "./pages/SignUpPage";
import { authGoogleCallback, getUserId } from "./services/auth-service";
import { useAuthStore } from "./stores/auth-store";
import { clearQueryParams } from "./utils/navigation";
import UserPostsPage from "./pages/users/PostsPage";

function App(): React.ReactNode {
    const navigate = useNavigate();
    const setUserId = useAuthStore((state) => state.setUserId);

    // Check if the user is logged in when the app loads
    useEffect(() => {
        async function initAuth(): Promise<void> {
            const userId = await getUserId();
            setUserId(userId);
        }
        initAuth();
    }, [setUserId]);

    // When the url contains OAuth callback parameters, attempt to authenticate the user with Google
    useEffect(() => {
        async function handleOAuthCallback(): Promise<void> {
            const url = new URL(window.location.href);
            const urlParams = new URLSearchParams(url.search);
            if (!urlParams.has("state") || !urlParams.has("code")) {
                return;
            }

            const query = window.location.search;
            try {
                await authGoogleCallback(query);
                const userId = await getUserId();
                setUserId(userId);
                navigate("/feed");
            } finally {
                clearQueryParams();
            }
        }

        handleOAuthCallback();
    }, [navigate, setUserId]);

    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route
                    index
                    element={
                        <UnauthenticatedRoute redirectTo="/feed">
                            <LandingPage />
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
                <Route
                    path="feed"
                    element={
                        <AuthenticatedRoute redirectTo="/">
                            <FeedPage />
                        </AuthenticatedRoute>
                    }
                />
                <Route path="account">
                    <Route
                        path="posts"
                        element={
                            <AuthenticatedRoute redirectTo="/">
                                <AccountPostPage />
                            </AuthenticatedRoute>
                        }
                    />
                    <Route
                        path="settings"
                        element={
                            <AuthenticatedRoute redirectTo="/">
                                <SettingsPage />
                            </AuthenticatedRoute>
                        }
                    />
                    <Route
                        path="saved"
                        element={
                            <AuthenticatedRoute redirectTo="/">
                                <SavedPostsPage />
                            </AuthenticatedRoute>
                        }
                    />
                </Route>
                <Route path="users">
                    <Route
                        path=":userId"
                        element={
                            <AuthenticatedRoute redirectTo="/">
                                <UserPostsPage />
                            </AuthenticatedRoute>
                        }
                    ></Route>
                </Route>
            </Route>
            <Route path="auth">
                <Route
                    path="login"
                    element={
                        <UnauthenticatedRoute redirectTo="/feed">
                            <LogInPage />
                        </UnauthenticatedRoute>
                    }
                />
                <Route
                    path="signup"
                    element={
                        <UnauthenticatedRoute redirectTo="/feed">
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
