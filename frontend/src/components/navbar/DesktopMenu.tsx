import { useIsAuthenticated } from "../../stores/auth-store";
import MenuLinks from "./MenuLinks";

function DesktopMenu(): React.ReactNode {
    const isAuthenticated = useIsAuthenticated();

    if (!isAuthenticated) {
        return null;
    }

    return (
        <ul className="menu menu-horizontal px-1 gap-1">
            <MenuLinks />
        </ul>
    );
}

export default DesktopMenu;
