import { RiMenu2Fill } from "react-icons/ri";
import { useIsAuthenticated } from "../../stores/auth-store";
import MenuLinks from "./MenuLinks";

function MobileMenu(): React.ReactNode {
    const isAuthenticated = useIsAuthenticated();

    if (!isAuthenticated) {
        return null;
    }

    return (
        <>
            <div tabIndex={0} role="button" className="btn btn-ghost md:hidden">
                <RiMenu2Fill className="text-2xl" />
            </div>
            <ul
                tabIndex={0}
                className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow"
            >
                <MenuLinks />
            </ul>
        </>
    );
}

export default MobileMenu;
