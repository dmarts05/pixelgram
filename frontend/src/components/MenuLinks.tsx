import React from "react";
import { NavLink } from "react-router";
import { MENU_LINKS } from "../utils/constants";

function Links(): React.ReactNode {
    return (
        <>
            {MENU_LINKS.map(({ path: to, name: label }) => (
                <li key={to}>
                    <NavLink
                        to={to}
                        className={({ isActive }) =>
                            isActive ? "font-bold" : ""
                        }
                    >
                        {label}
                    </NavLink>
                </li>
            ))}
        </>
    );
}

export default Links;
