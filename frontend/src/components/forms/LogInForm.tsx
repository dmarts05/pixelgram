import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import googleLogo from "../../assets/google-logo.webp";
import { authGoogle, logIn } from "../../services/auth-service";
import { useAuthStore } from "../../stores/auth-store";
import InputField from "./InputField";

export type LogInFormData = {
    email: string;
    password: string;
};

function LogInForm(): React.ReactNode {
    const navigate = useNavigate();

    const setIsAuthenticated = useAuthStore(
        (state) => state.setIsAuthenticated
    );

    const regularAuthMutation = useMutation({
        mutationFn: logIn,
        onSuccess: () => {
            setIsAuthenticated(true);
            navigate("/feed");
        },
    });

    const googleAuthMutation = useMutation({
        mutationFn: authGoogle,
    });

    function onSubmit(data: LogInFormData): void {
        regularAuthMutation.mutate(data);
    }

    function onGoogleLogIn(): void {
        googleAuthMutation.mutate();
    }

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LogInFormData>();

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-4"
            noValidate
        >
            {/* Email Field */}
            <InputField<LogInFormData>
                name="email"
                label="Email"
                type="email"
                register={register}
                error={errors.email}
                rules={{
                    required: "Email is required",
                    pattern: {
                        value: /^\S+@\S+$/i,
                        message: "Invalid email address",
                    },
                }}
            />

            {/* Password Field */}
            <InputField<LogInFormData>
                name="password"
                label="Password"
                type="password"
                register={register}
                error={errors.password}
                rules={{
                    required: "Password is required",
                }}
            />

            {/* Error Message */}
            {regularAuthMutation.isError && (
                <p className="text-error text-sm text-center">
                    {regularAuthMutation.error.message}
                </p>
            )}
            {googleAuthMutation.isError && (
                <p className="text-error text-sm text-center">
                    {googleAuthMutation.error.message}
                </p>
            )}

            {/* Submit Button */}
            <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={
                    regularAuthMutation.isPending ||
                    googleAuthMutation.isPending
                }
            >
                {regularAuthMutation.isPending ? (
                    <span className="loading loading-spinner loading-sm" />
                ) : (
                    <span className="text-sm font-medium">Log In</span>
                )}
            </button>

            {/* Divider */}
            <div className="flex items-center gap-2">
                <div className="flex-grow h-px bg-base-300" />
                <span className="text-sm text-secondary">or</span>
                <div className="flex-grow h-px bg-base-300" />
            </div>

            {/* Google Log In Button */}
            <button
                type="button"
                onClick={onGoogleLogIn}
                className="btn btn-outline flex items-center justify-center gap-2 w-full"
                disabled={
                    regularAuthMutation.isPending ||
                    googleAuthMutation.isPending
                }
            >
                <img src={googleLogo} alt="Google Logo" className="w-7 h-7" />
                {googleAuthMutation.isPending ? (
                    <span className="loading loading-spinner loading-sm" />
                ) : (
                    <span className="text-sm font-medium">
                        Log In with Google
                    </span>
                )}
            </button>
        </form>
    );
}

export default LogInForm;
