import { Link } from "react-router";
import BrandLogo from "../components/BrandLogo";
import SignUpForm from "../components/forms/SignUpForm";

function SignUpPage(): React.ReactNode {
    return (
        <div className="flex items-center justify-center min-h-dvh bg-base-200">
            <div className="card w-full max-w-md shadow-lg bg-base-100">
                <div className="card-body flex flex-column gap-4">
                    <BrandLogo
                        text="Sign Up"
                        direction="column"
                        textSize="2xl"
                        width={50}
                        height={50}
                    />
                    <SignUpForm />
                    <div className="text-center">
                        <span className="text-sm">Already registered? </span>
                        <Link to="/auth/login" className="link link-primary">
                            Log in
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SignUpPage;
