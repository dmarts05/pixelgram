import { ReactNode } from "react";
import { Navigate } from "react-router";
import { useAuthStore } from "../stores/auth-store";

interface UnauthenticatedRouteProps {
    children: ReactNode;
    redirectTo: string;
}

function UnauthenticatedRoute({
    children,
    redirectTo,
}: UnauthenticatedRouteProps): React.ReactNode {
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    if (isAuthenticated) {
        return <Navigate to={redirectTo} />;
    }
    return <>{children}</>;
}

export default UnauthenticatedRoute;
