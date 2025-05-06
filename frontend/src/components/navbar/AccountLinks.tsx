import React from "react";
import { NavLink } from "react-router";
import { ACCOUNT_LINKS } from "../../utils/constants";

function Links(): React.ReactNode {
    return (
        <>
            {ACCOUNT_LINKS.map(({ link: { path: to, name: label }, icon }) => (
                <li key={to}>
                    <NavLink
                        to={to}
                        className={({ isActive }) =>
                            isActive ? "font-bold" : ""
                        }
                    >
                        {React.createElement(icon)}
                        {label}
                    </NavLink>
                </li>
            ))}
        </>
    );
}

export default Links;
