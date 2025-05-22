import { Link } from "react-router";
import BrandLogo from "../components/BrandLogo";
import LogInForm from "../components/forms/LogInForm";

function LogInPage(): React.ReactNode {
    return (
        <div className="flex items-center justify-center min-h-svh bg-base-200">
            <div className="card w-full max-w-md shadow-lg bg-base-100">
                <div className="card-body flex flex-column gap-4">
                    <BrandLogo
                        text="Log In"
                        direction="column"
                        textSize="2xl"
                        width={50}
                        height={50}
                    />
                    <LogInForm />
                    <div className="text-center">
                        <span className="text-sm">Not registered? </span>
                        <Link to="/auth/signup" className="link link-primary">
                            Sign up
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LogInPage;
