import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import "./index.css";
import Layout from "./layouts/Layout.tsx";
import LandingPage from "./pages/LandingPage.tsx";
import LogInPage from "./pages/LogInPage.tsx";
import SignUpPage from "./pages/SignUpPage.tsx";

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <BrowserRouter>
            <Routes>
                <Route element={<Layout />}>
                    <Route index element={<LandingPage />} />
                </Route>
                <Route path="auth">
                    <Route path="login" element={<LogInPage />} />
                    <Route path="signup" element={<SignUpPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    </StrictMode>
);
