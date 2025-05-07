import { Tool } from "../../../types/tool";
import { TOOLBOX_COLORS } from "../../../utils/constants";
import ToolboxColorButton from "./ToolboxColorButton";
import ToolboxColorPicker from "./ToolboxColorPicker";
import ToolboxEraser from "./ToolboxEraser";
import ToolboxImageUploader from "./ToolboxImageUploader";
import ToolboxThicknessControl from "./ToolboxThicknessControl";

interface ToolboxProps {
    tool: Tool;
    setTool: React.Dispatch<React.SetStateAction<Tool>>;
    color: string;
    setColor: React.Dispatch<React.SetStateAction<string>>;
    pencilThickness: number;
    setPencilThickness: React.Dispatch<React.SetStateAction<number>>;
    handleImageUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

function Toolbox({
    tool,
    setTool,
    color,
    setColor,
    pencilThickness,
    setPencilThickness,
    handleImageUpload,
}: ToolboxProps): React.ReactElement {
    return (
        <aside className="flex flex-col gap-1">
            <ToolboxImageUploader
                inputId="image-input"
                handleImageUpload={handleImageUpload}
            />
            <ToolboxEraser selectedTool={tool} setTool={setTool} />
            {TOOLBOX_COLORS.map((c) => (
                <ToolboxColorButton
                    key={c}
                    selectedTool={tool}
                    selectedColor={color}
                    thisColor={c}
                    onSelect={(tool, color) => {
                        setTool(tool);
                        setColor(color);
                    }}
                />
            ))}
            <ToolboxColorPicker setTool={setTool} setColor={setColor} />
            <ToolboxThicknessControl
                thickness={pencilThickness}
                setThickness={setPencilThickness}
            />
        </aside>
    );
}

export default Toolbox;
