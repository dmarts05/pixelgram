import { Outlet } from "react-router";
import Navbar from "../components/Navbar";

function Layout(): React.ReactNode {
    return (
        <div className="min-h-screen">
            <Navbar />
            <Outlet />
        </div>
    );
}

export default Layout;
