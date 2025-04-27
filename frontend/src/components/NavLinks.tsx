import { JSX } from "react";
import { Link } from "react-router";

function NavLinks(): JSX.Element {
    return (
        <div className="flex items-center gap-2">
            <Link to="/auth/login" className="btn btn-secondary">
                Log In
            </Link>
            <Link to="/auth/signup" className="btn btn-primary">
                Sign Up
            </Link>
        </div>
    );
}

export default NavLinks;
