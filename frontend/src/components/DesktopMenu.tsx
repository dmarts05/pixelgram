import { useAuthStore } from "../stores/auth-store";
import MenuLinks from "./MenuLinks";

function DesktopMenu(): React.ReactNode {
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

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
