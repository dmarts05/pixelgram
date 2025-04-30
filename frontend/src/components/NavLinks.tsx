import { Link, useNavigate } from "react-router";
import { logout } from "../services/auth-service";
import { useAuthStore } from "../stores/auth-store";

function NavLinks(): React.ReactNode {
    const navigate = useNavigate();

    const { isAuthenticated, setIsAuthenticated } = useAuthStore();

    return (
        <div className="flex items-center gap-2">
            {!isAuthenticated && (
                <>
                    <Link to="/auth/login" className="btn btn-secondary">
                        Log In
                    </Link>
                    <Link to="/auth/signup" className="btn btn-primary">
                        Sign Up
                    </Link>
                </>
            )}
            {isAuthenticated && (
                <>
                    <button
                        className="btn btn-secondary"
                        onClick={async () => {
                            await logout();
                            setIsAuthenticated(false);
                            navigate("/");
                        }}
                    >
                        Log Out
                    </button>
                </>
            )}
        </div>
    );
}

export default NavLinks;
