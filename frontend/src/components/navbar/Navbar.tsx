import BrandLogo from "../BrandLogo";
import AuthMenu from "./AuthMenu";
import DesktopMenu from "./DesktopMenu";
import MobileMenu from "./MobileMenu";

function Navbar(): React.ReactNode {
    return (
        <nav className="navbar bg-base-100 shadow-sm">
            <div className="navbar-start sm:gap-2 gap-0">
                <div className="dropdown">
                    <MobileMenu />
                </div>
                <BrandLogo
                    enableLinkToHomeLogo={true}
                    enableLinkToHomeText={true}
                />
            </div>

            <div className="navbar-center hidden md:flex">
                <DesktopMenu />
            </div>

            <div className="navbar-end mr-7">
                <AuthMenu />
            </div>
        </nav>
    );
}

export default Navbar;
