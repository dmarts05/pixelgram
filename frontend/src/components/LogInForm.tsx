import { JSX } from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import googleLogo from "../assets/google-logo.webp";
import InputField from "./InputField";

type LogInFormData = {
    email: string;
    password: string;
};

function LogInForm(): JSX.Element {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LogInFormData>();

    const onSubmit: SubmitHandler<LogInFormData> = (data) => {
        console.log("Login Data:", data);
    };

    const handleGoogleLogIn = (): void => {
        // TODO
    };

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

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary w-full">
                Log In
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
                onClick={handleGoogleLogIn}
                className="btn btn-outline flex items-center justify-center gap-2 w-full"
            >
                <img src={googleLogo} alt="Google Logo" className="w-7 h-7" />
                <span className="text-sm font-medium">Log In with Google</span>
            </button>
        </form>
    );
}

export default LogInForm;
