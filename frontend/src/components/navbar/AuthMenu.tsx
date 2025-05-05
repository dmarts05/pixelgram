import { useMutation } from "@tanstack/react-query";
import { Link, useNavigate } from "react-router";
import { logout } from "../../services/auth-service";
import { useAuthStore } from "../../stores/auth-store";

function AuthMenu(): React.ReactNode {
    const navigate = useNavigate();
    const { isAuthenticated, setIsAuthenticated } = useAuthStore();

    const mutation = useMutation({
        mutationFn: logout,
        onSuccess: () => {
            setIsAuthenticated(false);
            navigate("/");
        },
    });

    return (
        <div className="flex items-center gap-2">
            {isAuthenticated ? (
                <button
                    className="btn btn-secondary"
                    onClick={() => mutation.mutate()}
                    disabled={mutation.isPending}
                >
                    Log Out
                </button>
            ) : (
                <>
                    <Link to="/auth/login" className="btn btn-secondary">
                        Log In
                    </Link>
                    <Link to="/auth/signup" className="btn btn-primary">
                        Get Started
                    </Link>
                </>
            )}
        </div>
    );
}

export default AuthMenu;
