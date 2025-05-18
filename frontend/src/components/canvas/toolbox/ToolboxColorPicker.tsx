import {GoPencil} from "react-icons/go";
import { Tool } from "../../../types/tool";

interface ToolboxColorPickerProps {
    selectedTool: Tool;
    setTool: (tool: Tool) => void;
    setColor: (color: string) => void;
}

function ToolboxColorPicker({
    selectedTool,
    setTool,
    setColor,
}: ToolboxColorPickerProps): React.ReactElement {
    const isSelected = selectedTool === "picker";
    return (
        <>
            <input
                type="color"
                id="colorPicker"
                className="hidden"
                onChange={(e) => {
                    setColor(e.target.value);
                }}
            />
            <button
                onClick={() => {document.getElementById("colorPicker")?.click();setTool("picker");}}
                className="btn btn-circle w-8 h-8 bg-gradient-to-r from-yellow-500 via-blue-500 to-purple-500 rainbow-animated"
            >{isSelected && <GoPencil className="stroke-2" />}</button>
        </>
    );
}

export default ToolboxColorPicker;
