import { JSX } from "react";

function NavButtons(): JSX.Element {
    return (
        <div className="flex items-center gap-2">
            <button className="btn btn-secondary">Log In</button>
            <button className="btn btn-primary">Sign Up</button>
        </div>
    );
}

export default NavButtons;
