import { Link } from "../types/link";

export const NAVBAR_HEIGHT = "4rem";

export const MENU_LINKS: Link[] = [
    { path: "/canvas", name: "Canvas" },
    { path: "/feed", name: "Feed" },
];

export const ACCOUNT_LINKS: Link[] = [
    { path: "/settings", name: "Settings" },
    { path: "/my-posts", name: "My posts" },
    { path: "/saved", name: "Saved" },
];

export const API_URL = import.meta.env.DEV
    ? "http://localhost:8000"
    : // Get production url from env
      import.meta.env.VITE_BACKEND_BASE_URL;
