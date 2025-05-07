import { NAVBAR_HEIGHT } from "../utils/constants";

function FullPageSpinner(): React.ReactNode {
    return (
        <div
            className="flex justify-center items-center"
            style={{
                height: `calc(100vh - ${NAVBAR_HEIGHT})`,
            }}
        >
            <span className="loading loading-ring loading-xl"></span>
        </div>
    );
}

export default FullPageSpinner;
