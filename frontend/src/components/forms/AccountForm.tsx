import { useMutation, useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { useAccountForm } from "../../hooks/useAccountForm";
import { getMyUser, updateUser } from "../../services/account-service";
import { AccountFormData } from "../../types/account";
import FullPageErrorAlert from "../FullPageErrorAlert";
import FullPageSpinner from "../FullPageSpinner";
import InputField from "./InputField";

function AccountForm(): React.ReactNode {
    const {
        data: userData,
        isLoading,
        isError,
        error,
    } = useQuery({
        queryKey: ["user"],
        queryFn: getMyUser,
    });

    const { register, handleSubmit, errors, reset, commonRules } =
        useAccountForm();

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

    const mutation = useMutation({
        mutationFn: updateUser,
    });

    function onSubmit(data: AccountFormData): void {
        const updateData: Partial<
            Pick<AccountFormData, "username" | "password">
        > = {
            ...(data.username !== userData?.username && {
                username: data.username,
            }),
            ...(data.password && { password: data.password }),
        };

        if (Object.keys(updateData).length > 0) {
            mutation.mutate(updateData);
        }
    }

    if (isLoading) {
        return <FullPageSpinner />;
    }

    if (isError) {
        return <FullPageErrorAlert errorMessage={String(error)} />;
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-4"
            noValidate
        >
            <InputField<AccountFormData>
                name="email"
                label="Email"
                type="email"
                register={register}
                error={errors.email}
                disabled={true}
                rules={commonRules.email}
            />

            <InputField<AccountFormData>
                name="username"
                label="Username"
                register={register}
                error={errors.username}
                rules={commonRules.username}
            />

            <InputField<AccountFormData>
                name="password"
                label="New password (leave blank to keep current)"
                type="password"
                register={register}
                error={errors.password}
                rules={{
                    ...commonRules.password,
                    required: false,
                }}
            />

            <InputField<AccountFormData>
                name="confirmPassword"
                label="Confirm Password"
                type="password"
                register={register}
                error={errors.confirmPassword}
                rules={commonRules.confirmPassword}
            />

            {mutation.isError && (
                <p className="text-error text-sm text-center">
                    {(mutation.error as Error).message}
                </p>
            )}
            {mutation.isSuccess && (
                <p className="text-success text-sm text-center">
                    Account updated successfully!
                </p>
            )}

            <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={mutation.isPending}
            >
                {mutation.isPending ? (
                    <span className="loading loading-spinner loading-sm" />
                ) : (
                    <span className="text-sm font-medium">Save</span>
                )}
            </button>
        </form>
    );
}

export default AccountForm;
