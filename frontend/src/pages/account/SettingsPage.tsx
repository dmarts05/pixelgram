import AccountForm from "../../components/forms/AccountForm";
import { NAVBAR_HEIGHT } from "../../utils/constants";
import ConfirmDeleteAccountModal from "../../components/account/ConfirmDeleteAccountModal";
import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { deleteAccount, getMyUser } from "../../services/account-service";
import { useAuthStore } from "../../stores/auth-store";
import FullPageSpinner from "../../components/FullPageSpinner";

function SettingsPage(): React.ReactNode {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const setUserId = useAuthStore((state) => state.setUserId);

    const mutation = useMutation({
        mutationFn: deleteAccount,
        onSuccess: () => {
            setUserId(null);
        },
    });

    const { isLoading } = useQuery({
        queryKey: ["user"],
        queryFn: getMyUser,
    });

    if (isLoading) {
        return <FullPageSpinner />;
    }

    return (
        <main
            className="flex justify-center"
            style={{
                marginTop: NAVBAR_HEIGHT,
            }}
        >
            <div className="card w-full max-w-md shadow-lg bg-base-100">
                <div className="card-body flex flex-column gap-4">
                    <h2 className="text-2xl text-center font-bold">Settings</h2>
                    <AccountForm />
                    <button
                        className="btn btn-error"
                        onClick={() => setIsModalOpen(true)}
                        type="button"
                    >
                        Delete account
                    </button>
                </div>
            </div>
            <ConfirmDeleteAccountModal
                isOpen={isModalOpen}
                onCancel={() => setIsModalOpen(false)}
                onConfirm={() => mutation.mutate()}
                isLoading={mutation.isPending}
            />
        </main>
    );
}

export default SettingsPage;
