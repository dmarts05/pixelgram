import AccountForm from "../../components/forms/AccountForm";

function SettingsPage(): React.ReactNode {
    return (
        <div className="flex items-center justify-center min-h-screen bg-base-200">
            <div className="card w-full max-w-md shadow-lg bg-base-100">
                <div className="card-body flex flex-column gap-4">
                    <AccountForm />
                </div>
            </div>
        </div>
    );
}

export default SettingsPage;
