import { Link } from "../types/link";

export const NAVBAR_HEIGHT = "4rem";

export const MENU_LINKS: Link[] = [
    { path: "/canvas", name: "Canvas" },
    { path: "/feed", name: "Feed" },
];

export const API_URL = import.meta.env.DEV
    ? "http://localhost:8000"
    : "https://pixelgram-backend.onrender.com";
