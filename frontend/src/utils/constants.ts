import { RiBookmarkLine, RiSettingsLine, RiImageLine } from "react-icons/ri";
import { Link, LinkWithIcon } from "../types/link";

export const NAVBAR_HEIGHT = "4rem";

export const MENU_LINKS: Link[] = [
    { path: "/canvas", name: "Canvas" },
    { path: "/feed", name: "Feed" },
];

export const ACCOUNT_LINKS: LinkWithIcon[] = [
    {
        link: { path: "/account/settings", name: "Settings" },
        icon: RiSettingsLine,
    },
    { link: { path: "/account/posts", name: "My posts" }, icon: RiImageLine },

    { link: { path: "/account/saved", name: "Saved" }, icon: RiBookmarkLine },
];

export const API_URL = import.meta.env.DEV
    ? "http://localhost:8000"
    : // Get production url from env
      import.meta.env.VITE_BACKEND_BASE_URL;
