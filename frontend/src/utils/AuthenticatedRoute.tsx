import { JSX, ReactNode } from "react";
import { Navigate } from "react-router";
import { useAuthStore } from "../stores/auth-store";

interface AuthenticatedRouteProps {
    children: ReactNode;
    redirectTo: string;
}

function AuthenticatedRoute({
    children,
    redirectTo,
}: AuthenticatedRouteProps): JSX.Element {
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    if (!isAuthenticated) {
        return <Navigate to={redirectTo} />;
    }
    return <>{children}</>;
}

export default AuthenticatedRoute;
