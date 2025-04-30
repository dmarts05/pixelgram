import { NAVBAR_HEIGHT } from "../utils/constants";
import BrandLogo from "./BrandLogo";
import NavLinks from "./NavLinks";

function Navbar(): React.ReactNode {
    return (
        <nav
            className="bg-base-100 shadow-md p-4 md:px-8 flex justify-between align-middle"
            style={{ height: NAVBAR_HEIGHT }}
        >
            <BrandLogo />
            <NavLinks />
        </nav>
    );
}

export default Navbar;
