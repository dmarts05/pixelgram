interface ToolboxThicknessControlProps {
    thickness: number;
    setThickness: (value: number) => void;
}

function ToolboxThicknessControl({
    thickness,
    setThickness,
}: ToolboxThicknessControlProps): React.ReactNode {
    return (
        <div className="flex flex-col w-8 items-center gap-4">
            <button
                className="btn btn-circle w-8 h-8 border-white border-2"
                onClick={() => setThickness(Math.max(1, thickness - 1))}
            >
                -
            </button>
            <input
                type="range"
                min="1"
                max="20"
                value={thickness}
                onChange={(e) => setThickness(Number(e.target.value))}
                className="range range-primary w-24 mt-6 mb-6"
                style={{ transform: "rotate(90deg)" }}
            />
            <button
                className="btn btn-circle w-8 h-8 border-white border-2"
                onClick={() => setThickness(Math.min(20, thickness + 1))}
            >
                +
            </button>
        </div>
    );
}

export default ToolboxThicknessControl;
