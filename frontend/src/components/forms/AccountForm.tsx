import { useMutation, useQuery } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { useEffect } from "react";
import { getMyUser, updateUser } from "../../services/account-service";
import InputField from "./InputField";
import { AccountFormData } from "../../types/account";

function AccountForm(): React.ReactNode {
    const { data: userData, isLoading } = useQuery({
        queryKey: ["user"],
        queryFn: getMyUser,
    });

    const {
        register,
        handleSubmit,
        formState: { errors },
        watch,
        reset,
    } = useForm<AccountFormData>();

    useEffect(() => {
        if (userData) {
            reset({
                email: userData.email,
                username: userData.username,
                password: "",
                confirmPassword: "",
            });
        }
    }, [userData, reset]);

    const updateMutation = useMutation({
        mutationFn: updateUser,
        onSuccess: () => {
            // TODO: Show success message and redirect to feed
        },
    });

    const usernameValue = watch("username");
    const emailValue = watch("email");
    const passwordValue = watch("password");

    function onSubmit(data: AccountFormData): void {
        // Only send changed fields
        const updateData = {
            ...(data.username !== userData?.username && {
                username: data.username,
            }),
            ...(data.password && { password: data.password }),
        };

        if (Object.keys(updateData).length > 0) {
            updateMutation.mutate(updateData);
        }
    }

    if (isLoading) {
        return (
            <div className="flex justify-center">
                <span className="loading loading-spinner loading-lg"></span>
            </div>
        );
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-4"
            noValidate
        >
            {/* Email Field (read-only) */}
            <InputField<AccountFormData>
                name="email"
                label="Email"
                type="email"
                register={register}
                error={errors.email}
                disabled={true}
                rules={{
                    required: "Email is required",
                    pattern: {
                        value: /^\S+@\S+$/i,
                        message: "Invalid email address",
                    },
                }}
            />

            {/* Username Field */}
            <InputField<AccountFormData>
                name="username"
                label="username"
                register={register}
                error={errors.username}
                rules={{
                    required: "Username is required",
                }}
            />

            {/* Password Field (optional for updates) */}
            <InputField<AccountFormData>
                name="password"
                label="New password (leave blank to keep current)"
                type="password"
                register={register}
                error={errors.password}
                rules={{
                    minLength: {
                        value: 8,
                        message: "Password must be at least 8 characters",
                    },
                    validate: (value: string) => {
                        if (!value) return true;

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
            <InputField<AccountFormData>
                name="confirmPassword"
                label="Confirm Password"
                type="password"
                register={register}
                error={errors.confirmPassword}
                rules={{
                    validate: (value: string) => {
                        if (!passwordValue) return true;
                        return (
                            value === passwordValue || "Passwords do not match"
                        );
                    },
                }}
            />

            {/* Error/Success messages */}
            {updateMutation.isError && (
                <p className="text-error text-sm text-center">
                    {updateMutation.error.message}
                </p>
            )}
            {updateMutation.isSuccess && (
                <p className="text-success text-sm text-center">
                    Account updated successfully!
                </p>
            )}

            {/* Submit Button */}
            <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={updateMutation.isPending}
            >
                {updateMutation.isPending ? (
                    <span className="loading loading-spinner loading-sm" />
                ) : (
                    <span className="text-sm font-medium">Save</span>
                )}
            </button>
        </form>
    );
}

export default AccountForm;
