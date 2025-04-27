import { useMutation } from "@tanstack/react-query";
import { JSX } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import googleLogo from "../assets/google-logo.webp";
import { authGoogle, signUp } from "../services/auth-service";
import InputField from "./InputField";

export type SignUpFormData = {
    username: string;
    email: string;
    password: string;
    confirmPassword: string;
};

function SignUpForm(): JSX.Element {
    const navigate = useNavigate();

    const regularAuthMutation = useMutation({
        mutationFn: signUp,
        onSuccess: () => {
            navigate("/auth/login");
        },
    });

    const googleAuthMutation = useMutation({
        mutationFn: authGoogle,
    });

    function onSubmit(data: SignUpFormData): void {
        regularAuthMutation.mutate(data);
    }

    function onGoogleSignUp(): void {
        googleAuthMutation.mutate();
    }

    const {
        register,
        handleSubmit,
        formState: { errors },
        watch,
    } = useForm<SignUpFormData>();

    const usernameValue = watch("username");
    const emailValue = watch("email");
    const passwordValue = watch("password");

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-4"
            noValidate
        >
            {/* Email Field */}
            <InputField<SignUpFormData>
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

            {/* Username Field */}
            <InputField<SignUpFormData>
                name="username"
                label="Username"
                register={register}
                error={errors.username}
                rules={{
                    required: "Username is required",
                }}
            />

            {/* Password Field */}
            <InputField<SignUpFormData>
                name="password"
                label="Password"
                type="password"
                register={register}
                error={errors.password}
                rules={{
                    required: "Password is required",
                    minLength: {
                        value: 8,
                        message: "Password must be at least 8 characters",
                    },
                    validate: (value: string) => {
                        const isUsernameInPassword =
                            usernameValue &&
                            value
                                .toLowerCase()
                                .includes(usernameValue.toLowerCase());
                        const isEmailInPassword =
                            emailValue &&
                            value
                                .toLowerCase()
                                .includes(emailValue.split("@")[0]);

                        if (isUsernameInPassword) {
                            return "Password cannot contain your username";
                        }
                        if (isEmailInPassword) {
                            return "Password cannot contain your email";
                        }
                        return true;
                    },
                }}
            />

            {/* Confirm Password Field */}
            <InputField<SignUpFormData>
                name="confirmPassword"
                label="Confirm Password"
                type="password"
                register={register}
                error={errors.confirmPassword}
                rules={{
                    required: "Please confirm your password",
                    validate: (value: string) =>
                        value === passwordValue || "Passwords do not match",
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
                    <span className="text-sm font-medium">Sign Up</span>
                )}
            </button>

            {/* Divider */}
            <div className="flex items-center gap-2">
                <div className="flex-grow h-px bg-base-300" />
                <span className="text-sm text-secondary">or</span>
                <div className="flex-grow h-px bg-base-300" />
            </div>

            {/* Google Sign Up Button */}
            <button
                type="button"
                onClick={onGoogleSignUp}
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
                        Sign Up with Google
                    </span>
                )}
            </button>
        </form>
    );
}

export default SignUpForm;
