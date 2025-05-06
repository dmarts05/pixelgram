import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { authGoogle, signUp } from "../../services/auth-service";
import googleLogo from "../../assets/google-logo.webp";
import InputField from "./InputField";
import { AccountFormData } from "../../types/account";
import { useAccountForm } from "../../hooks/useAccountForm";

function SignUpForm(): React.ReactNode {
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

    function onSubmit(data: AccountFormData): void {
        regularAuthMutation.mutate(data);
    }

    function onGoogleSignUp(): void {
        googleAuthMutation.mutate();
    }

    const { register, handleSubmit, errors, commonRules } = useAccountForm();

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-4"
            noValidate
        >
            {/* Email Field */}
            <InputField<AccountFormData>
                name="email"
                label="Email"
                type="email"
                register={register}
                error={errors.email}
                rules={commonRules.email}
            />

            {/* Username Field */}
            <InputField<AccountFormData>
                name="username"
                label="Username"
                register={register}
                error={errors.username}
                rules={commonRules.username}
            />

            {/* Password Field */}
            <InputField<AccountFormData>
                name="password"
                label="Password"
                type="password"
                register={register}
                error={errors.password}
                rules={commonRules.password}
            />

            {/* Confirm Password Field */}
            <InputField<AccountFormData>
                name="confirmPassword"
                label="Confirm Password"
                type="password"
                register={register}
                error={errors.confirmPassword}
                rules={{
                    required: "Please confirm your password",
                    ...commonRules.confirmPassword,
                }}
            />

            {/* Error Message */}
            {regularAuthMutation.isError && (
                <p className="text-error text-sm text-center">
                    {(regularAuthMutation.error as Error).message}
                </p>
            )}
            {googleAuthMutation.isError && (
                <p className="text-error text-sm text-center">
                    {(googleAuthMutation.error as Error).message}
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
