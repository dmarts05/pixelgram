import React, { useState } from "react";
import Canvas from "../components/canvas/Canvas";
import Toolbox from "../components/canvas/toolbox/Toolbox";
import PublishPixelartModal from "../components/forms/PublishPixelartModal";
import { NAVBAR_HEIGHT } from "../utils/constants";

function CanvasPage(): React.ReactNode {
    const [tool, setTool] = useState<"pencil" | "eraser" | "picker">("pencil");
    const [color, setColor] = useState<string>("#000000");
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [imageUrl, setImageUrl] = useState<string>("");
    const [pencilThickness, setPencilThickness] = useState<number>(5);

    const canvasRef = React.useRef<HTMLCanvasElement | null>(null);

    function handleImageUpload(e: React.ChangeEvent<HTMLInputElement>): void {
        const file = e.target.files?.[0];
        if (!file) {
            return;
        }

        const reader = new FileReader();
        reader.onload = (event): void => {
            const img = new Image();
            img.src = event.target?.result as string;
            img.onload = (): void => {
                const canvas = canvasRef.current;
                const context = canvas?.getContext("2d");
                if (!canvas || !context) {
                    return;
                }
                context.drawImage(img, 0, 0, canvas.width, canvas.height);
            };
            if (reader.result) {
                img.src = reader.result as string;
            }
        };
        reader.readAsDataURL(file);
    }

    function handlePublish(): void {
        const canvas = canvasRef.current;
        if (!canvas) {
            return;
        }

        const dataURL = canvas.toDataURL("image/png");
        setImageUrl(dataURL);
        setIsModalOpen(true);
    }

    return (
        <>
            <main
                className="flex justify-center items-center gap-4 p-4"
                style={{ height: `calc(100svh - ${NAVBAR_HEIGHT} - 1px)` }}
            >
                <Toolbox
                    tool={tool}
                    setTool={setTool}
                    color={color}
                    setColor={setColor}
                    pencilThickness={pencilThickness}
                    setPencilThickness={setPencilThickness}
                    handleImageUpload={handleImageUpload}
                />

                <Canvas
                    canvasRef={canvasRef}
                    color={color}
                    pencilThickness={pencilThickness}
                    tool={tool}
                    onPublish={handlePublish}
                />
            </main>
            <PublishPixelartModal
                imageUrl={imageUrl}
                isOpen={isModalOpen}
                onClose={(): void => setIsModalOpen(false)}
            />
        </>
    );
}

export default CanvasPage;
