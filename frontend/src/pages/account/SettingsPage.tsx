import AccountForm from "../../components/forms/AccountForm";
import { NAVBAR_HEIGHT } from "../../utils/constants";

function SettingsPage(): React.ReactNode {
    return (
        <main
            className="flex items-center justify-center"
            style={{
                height: `calc(100vh - ${NAVBAR_HEIGHT})`,
            }}
        >
            <div className="card w-full max-w-md shadow-lg bg-base-100">
                <div className="card-body flex flex-column gap-4">
                    <h2 className="text-2xl text-center font-bold">Settings</h2>
                    <AccountForm />
                </div>
            </div>
        </main>
    );
}

export default SettingsPage;
