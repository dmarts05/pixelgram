import { useForm, FieldErrors } from "react-hook-form";
import { AccountFormData } from "../types/account";

interface UseAccountFormReturn {
    register: ReturnType<typeof useForm<AccountFormData>>["register"];
    handleSubmit: ReturnType<typeof useForm<AccountFormData>>["handleSubmit"];
    errors: FieldErrors<AccountFormData>;
    reset: ReturnType<typeof useForm<AccountFormData>>["reset"];
    emailValue: string;
    usernameValue: string;
    passwordValue: string;
    commonRules: {
        email: object;
        username: object;
        password: object;
        confirmPassword: object;
    };
}

export function useAccountForm(
    defaultValues?: Partial<AccountFormData>
): UseAccountFormReturn {
    const {
        register,
        handleSubmit,
        formState: { errors },
        watch,
        reset,
    } = useForm<AccountFormData>({ defaultValues });

    const emailValue = watch("email");
    const usernameValue = watch("username");
    const passwordValue = watch("password");

    const commonRules = {
        email: {
            required: "Email is required",
            pattern: {
                value: /^\S+@\S+$/i,
                message: "Invalid email address",
            },
        },
        username: {
            required: "Username is required",
        },
        password: {
            required: "Password is required",
            minLength: {
                value: 8,
                message: "Password must be at least 8 characters",
            },
            validate: (value: string): true | string => {
                if (!value) return true;

                if (
                    usernameValue &&
                    value.toLowerCase().includes(usernameValue.toLowerCase())
                ) {
                    return "Password cannot contain your username";
                }
                if (
                    emailValue &&
                    value.toLowerCase().includes(emailValue.split("@")[0])
                ) {
                    return "Password cannot contain your email";
                }
                return true;
            },
        },
        confirmPassword: {
            validate: (value: string): true | string =>
                value === passwordValue || "Passwords do not match",
        },
    };

    return {
        register,
        handleSubmit,
        errors,
        reset,
        emailValue,
        usernameValue,
        passwordValue,
        commonRules,
    };
}
