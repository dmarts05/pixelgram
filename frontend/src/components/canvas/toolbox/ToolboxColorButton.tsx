import { GoPencil } from "react-icons/go";
import { Tool } from "../../../types/tool";

interface ToolboxColorButtonProps {
    selectedTool: Tool;
    selectedColor: string;
    thisColor: string;
    onSelect: (tool: Tool, color: string) => void;
}

function ToolboxColorButton({
    selectedTool,
    selectedColor,
    thisColor,
    onSelect,
}: ToolboxColorButtonProps): React.ReactNode {
    const isSelected = selectedTool === "pencil" && selectedColor === thisColor;

    return (
        <button
            onClick={() => onSelect("pencil", thisColor)}
            className={`btn btn-circle w-8 h-8 border-white border-2`}
            style={{ backgroundColor: thisColor }}
        >
            {isSelected && <GoPencil className={`stroke-2 ${thisColor === "#000000" ? "text-white" : ""}`} />}
        </button>
    );
}

export default ToolboxColorButton;
