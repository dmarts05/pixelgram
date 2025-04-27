import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import "./index.css";
import Layout from "./layouts/Layout.tsx";
import LandingPage from "./pages/LandingPage.tsx";

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <BrowserRouter>
            <Routes>
                <Route element={<Layout />}>
                    <Route index element={<LandingPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    </StrictMode>
);
