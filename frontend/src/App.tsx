import { JSX, useEffect } from "react";
import { Navigate, Route, Routes } from "react-router";
import Layout from "./layouts/Layout";
import LandingPage from "./pages/LandingPage";
import LogInPage from "./pages/LogInPage";
import NotFoundPage from "./pages/NotFoundPage";
import SignUpPage from "./pages/SignUpPage";
import { isUserLoggedIn } from "./services/auth-service";
import { useAuthStore } from "./stores/auth-store";

function App(): JSX.Element {
    const { isAuthenticated, setIsAuthenticated: setAuthenticated } =
        useAuthStore();

    useEffect(() => {
        async function initAuth(): Promise<void> {
            const isLoggedIn = await isUserLoggedIn();
            setAuthenticated(isLoggedIn);
        }
        initAuth();
    }, [setAuthenticated]);

    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route
                    index
                    element={
                        isAuthenticated ? (
                            <Navigate to="/canvas" />
                        ) : (
                            <LandingPage />
                        )
                    }
                />
            </Route>
            <Route path="auth">
                <Route
                    path="login"
                    element={
                        isAuthenticated ? (
                            <Navigate to="/canvas" />
                        ) : (
                            <LogInPage />
                        )
                    }
                />
                <Route
                    path="signup"
                    element={
                        isAuthenticated ? (
                            <Navigate to="/canvas" />
                        ) : (
                            <SignUpPage />
                        )
                    }
                />
            </Route>
            <Route path="canvas" element={<div>Canvas</div>} />
            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    );
}

export default App;
