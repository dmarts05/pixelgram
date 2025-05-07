import { BsFillEraserFill } from "react-icons/bs";
import { Tool } from "../../../types/tool";

type ToolboxEraserProps = {
    selectedTool: Tool;
    setTool: React.Dispatch<React.SetStateAction<Tool>>;
};

function ToolboxEraser({
    selectedTool,
    setTool,
}: ToolboxEraserProps): React.ReactNode {
    return (
        <button
            onClick={() => {
                setTool("eraser");
            }}
            className={`btn btn-circle w-8 h-8 border-white border-2 ${selectedTool === "eraser" ? "bg-black" : ""}`}
        >
            <BsFillEraserFill
                className={selectedTool === "eraser" ? "text-white" : ""}
            />
        </button>
    );
}

export default ToolboxEraser;
