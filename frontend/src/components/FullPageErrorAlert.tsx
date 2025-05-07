import { MdErrorOutline } from "react-icons/md";
import { NAVBAR_HEIGHT } from "../utils/constants";

type FullPageErrorAlertProps = {
    errorMessage: string;
};

function FullPageErrorAlert({
    errorMessage,
}: FullPageErrorAlertProps): React.ReactNode {
    return (
        <div
            className="flex justify-center items-center"
            style={{
                height: `calc(100vh - ${NAVBAR_HEIGHT})`,
            }}
        >
            <div
                role="alert"
                className="alert alert-error alert-soft !shadow-md w-80"
            >
                <MdErrorOutline className="text-xl" />
                <span>{errorMessage}</span>
            </div>
        </div>
    );
}

export default FullPageErrorAlert;
