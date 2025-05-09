import { useMutation } from "@tanstack/react-query";
import { RiAccountCircleLine, RiLogoutBoxRLine } from "react-icons/ri";
import { Link, useNavigate } from "react-router";
import { logout } from "../../services/auth-service";
import { useAuthStore, useIsAuthenticated } from "../../stores/auth-store";
import AccountLinks from "./AccountLinks";

function AuthMenu(): React.ReactNode {
    const navigate = useNavigate();
    const { setUserId } = useAuthStore();
    const isAuthenticated = useIsAuthenticated();

    const mutation = useMutation({
        mutationFn: logout,
        onSuccess: () => {
            setUserId(null);
            navigate("/");
        },
    });

    return (
        <>
            {isAuthenticated ? (
                <div className="dropdown dropdown-end">
                    <div tabIndex={0} role="button" className="btn btn-ghost">
                        <RiAccountCircleLine className="text-2xl" />
                    </div>
                    <ul
                        tabIndex={0}
                        className="menu dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow"
                    >
                        <AccountLinks />
                        <li>
                            <button
                                className=""
                                onClick={() => mutation.mutate()}
                                disabled={mutation.isPending}
                            >
                                <RiLogoutBoxRLine />
                                Log Out
                            </button>
                        </li>
                    </ul>
                </div>
            ) : (
                <div className="flex items-center gap-2">
                    <Link to="/auth/login" className="btn btn-secondary">
                        Log In
                    </Link>
                    <Link to="/auth/signup" className="btn btn-primary">
                        Get Started
                    </Link>
                </div>
            )}
        </>
    );
}

export default AuthMenu;
