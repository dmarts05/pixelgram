import AuthMenu from "./AuthMenu";
import BrandLogo from "./BrandLogo";
import DesktopMenu from "./DesktopMenu";
import MobileMenu from "./MobileMenu";

function Navbar(): React.ReactNode {
    return (
        <nav className="navbar bg-base-100 shadow-sm">
            <div className="navbar-start gap-2">
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

            <div className="navbar-end">
                <AuthMenu />
            </div>
        </nav>
    );
}

export default Navbar;
