import { Outlet } from "react-router";
import Navbar from "../components/navbar/Navbar";

function Layout(): React.ReactNode {
    return (
        <div className="min-h-svh bg-base-200">
            <Navbar />
            <Outlet />
        </div>
    );
}

export default Layout;
