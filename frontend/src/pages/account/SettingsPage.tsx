import { Link } from "react-router";
import BrandLogo from "../../components/BrandLogo";
import SignUpForm from "../../components/forms/SignUpForm";

function SettingsPage(): React.ReactNode {
    return (
        <div className="flex items-center justify-center min-h-screen bg-base-200">
            <div className="card w-full max-w-md shadow-lg bg-base-100">
                <div className="card-body flex flex-column gap-4">
                    <SignUpForm />
                </div>
            </div>
        </div>
    );
}

export default SettingsPage;
