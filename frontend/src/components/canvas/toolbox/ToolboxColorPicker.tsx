import { Tool } from "../../../types/tool";

interface ToolboxColorPickerProps {
    setTool: (tool: Tool) => void;
    setColor: (color: string) => void;
}

function ToolboxColorPicker({
    setTool,
    setColor,
}: ToolboxColorPickerProps): React.ReactElement {
    return (
        <>
            <input
                type="color"
                id="colorPicker"
                className="hidden"
                onChange={(e) => {
                    setTool("pencil");
                    setColor(e.target.value);
                }}
            />
            <button
                onClick={() => document.getElementById("colorPicker")?.click()}
                className="btn btn-circle w-8 h-8 bg-gradient-to-r from-yellow-500 via-blue-500 to-purple-500 rainbow-animated"
            ></button>
        </>
    );
}

export default ToolboxColorPicker;
