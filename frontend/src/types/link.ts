import { IconType } from "react-icons";

export type Link = {
    path: string;
    name: string;
};

export type LinkWithIcon = {
    link: Link;
    icon: IconType;
};
