import { Navigate } from "react-router";
import { useIsAuthenticated } from "../stores/auth-store";

type UnauthenticatedRouteProps = {
    children: React.ReactNode;
    redirectTo: string;
};

function UnauthenticatedRoute({
    children,
    redirectTo,
}: UnauthenticatedRouteProps): React.ReactNode {
    const isAuthenticated = useIsAuthenticated();

    if (isAuthenticated) {
        return <Navigate to={redirectTo} />;
    }
    return <>{children}</>;
}

export default UnauthenticatedRoute;
