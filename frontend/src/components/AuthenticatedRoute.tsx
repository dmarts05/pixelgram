import { ReactNode } from "react";
import { Navigate } from "react-router";
import { useIsAuthenticated } from "../stores/auth-store";

interface AuthenticatedRouteProps {
    children: ReactNode;
    redirectTo: string;
}

function AuthenticatedRoute({
    children,
    redirectTo,
}: AuthenticatedRouteProps): React.ReactNode {
    const isAuthenticated = useIsAuthenticated();

    if (!isAuthenticated) {
        return <Navigate to={redirectTo} />;
    }
    return <>{children}</>;
}

export default AuthenticatedRoute;
