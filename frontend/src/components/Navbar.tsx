import { JSX } from "react";
import { NAVBAR_HEIGHT } from "../utils/constants";
import LogoText from "./LogoText";
import NavButtons from "./NavButtons";

function Navbar(): JSX.Element {
    return (
        <nav
            className="bg-base-100 shadow-md p-4 md:px-8 flex justify-between align-middle"
            style={{ height: NAVBAR_HEIGHT }}
        >
            <LogoText />
            <NavButtons />
        </nav>
    );
}

export default Navbar;
