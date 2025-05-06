import React, { useEffect, useState } from "react";
import { BsFillEraserFill } from "react-icons/bs";
import { GoPencil } from "react-icons/go";
import { MdOutlineUploadFile } from "react-icons/md";
import PublishPixelartModal from "../components/forms/PublishPixelartModal";
import { NAVBAR_HEIGHT } from "../utils/constants";

function CanvasPage(): React.ReactElement {
    const [tool, setTool] = useState<"pencil" | "eraser">("pencil");
    const [color, setColor] = useState<string>("#000000");
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [imageUrl, setImageUrl] = useState<string>("");
    const [pencilThickness, setPencilThickness] = useState<number>(5);

    const canvasRef = React.useRef<HTMLCanvasElement | null>(null);
    const contextRef = React.useRef<CanvasRenderingContext2D | null>(null);

    // Load canvas in init
    useEffect(() => {
        const canvas = canvasRef.current;
        if (canvas) {
            const context = canvas.getContext("2d");
            if (context) {
                // Set canvas background color
                context.fillStyle = "rgba(0,0,0,1)";
                context.fillRect(0, 0, canvas.width, canvas.height);
                canvas.width = 128;
                canvas.height = 128;

                function resizeCanvas(): void {
                    const size =
                        Math.min(window.innerWidth, window.innerHeight) * 0.75;
                    if (canvas && context) {
                        canvas.style.width = `${size}px`;
                        canvas.style.height = `${size}px`;

                        context.imageSmoothingEnabled = false;

                        // Store the context to allow changing the color and tool
                        contextRef.current = context;
                    }
                }

                // Initial canvas size
                resizeCanvas();

                //TODO: See if conserve real time resize and erase all content or not resize and preserve content
                window.addEventListener("resize", resizeCanvas);

                return (): void => {
                    window.removeEventListener("resize", resizeCanvas);
                };
            }
        }
    }, []);

    // Load tools and methods to draw on canvas when changing tool or color
    useEffect(() => {
        const canvas = canvasRef.current;
        const context = contextRef.current;
        if (canvas && context) {
            let drawing = false;

            function getTouchPos(e: TouchEvent): { x: number; y: number } {
                if (canvas) {
                    const rect = canvas?.getBoundingClientRect();
                    const touch = e.touches[0];
                    const scaleX = canvas?.width / rect?.width || 1; // relationship bitmap vs. element for X
                    const scaleY = canvas?.height / rect?.height || 1; // relationship bitmap vs. element for Y

                    return {
                        x: (touch?.clientX - rect?.left) * scaleX || 1,
                        y: (touch?.clientY - rect?.top) * scaleY || 1,
                    };
                }
                return { x: 0, y: 0 };
            }

            function draw(e: MouseEvent | TouchEvent): void {
                if (!drawing) return;

                const rect = canvas?.getBoundingClientRect();
                let x, y;
                if (canvas && rect) {
                    if (e instanceof TouchEvent) {
                        const pos = getTouchPos(e);
                        x = pos.x;
                        y = pos.y;
                    } else {
                        const scaleX = canvas?.width / rect.width || 1; // relationship bitmap vs. element for X
                        const scaleY = canvas?.height / rect?.height || 1; // relationship bitmap vs. element for Y
                        x = (e.clientX - rect.left) * scaleX || 1;
                        y = (e.clientY - rect.top) * scaleY || 1;
                    }

                    if (context) {
                        context.lineWidth = pencilThickness;
                        context.lineCap = "round";

                        context.strokeStyle =
                            tool === "eraser" ? "rgba(0,0,0,1)" : color;
                        context.globalCompositeOperation =
                            tool === "eraser"
                                ? "destination-out"
                                : "source-over";

                        context.lineTo(x, y);
                        context.stroke();
                        context.beginPath();
                        context.moveTo(x, y);
                    }
                }
            }

            function startDrawing(e: MouseEvent | TouchEvent): void {
                drawing = true;
                draw(e);
            }

            function stopDrawing(): void {
                drawing = false;
                context?.beginPath();
            }

            // Mouse
            canvas.addEventListener("mousedown", startDrawing);
            canvas.addEventListener("mouseup", stopDrawing);
            canvas.addEventListener("mousemove", draw);

            canvas.addEventListener("touchstart", startDrawing);
            canvas.addEventListener("touchend", stopDrawing);
            canvas.addEventListener("touchmove", draw);

            return (): void => {
                canvas.removeEventListener("mousedown", startDrawing);
                canvas.removeEventListener("mouseup", stopDrawing);
                canvas.removeEventListener("mousemove", draw);

                canvas.removeEventListener("touchstart", startDrawing);
                canvas.removeEventListener("touchend", stopDrawing);
                canvas.removeEventListener("touchmove", draw);
            };
        }
    }, [color, tool, pencilThickness]);

    // Upload image to canvas, applying resolution change
    function handleImageUpload(e: React.ChangeEvent<HTMLInputElement>): void {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event): void => {
                const img = new Image();
                img.src = event.target?.result as string;
                img.onload = (): void => {
                    const canvas = document.getElementById(
                        "canvas"
                    ) as HTMLCanvasElement;
                    if (canvas) {
                        const context = canvas.getContext("2d");
                        if (context) {
                            context.drawImage(
                                img,
                                0,
                                0,
                                canvas.width,
                                canvas.height
                            );
                        }
                    }
                };
                if (reader.result) {
                    img.src = reader.result as string;
                }
            };
            reader.readAsDataURL(file);
        }
        return;
    }

    // Handle submit form (Click on publish button)
    function handleSubmit(e: React.FormEvent<HTMLFormElement>): void {
        e.preventDefault();

        const canvas = canvasRef.current;

        if (canvas) {
            const dataURL = canvas.toDataURL("image/png");
            setImageUrl(dataURL);
            setIsModalOpen(true);
        }
    }

    // Close publish modal handler
    const handleCloseModal = (): void => {
        setIsModalOpen(false);
    };

    return (
        <div
            className="flex flex-row bg-base-200 m-4"
            style={{ maxHeight: `calc(100vh - ${NAVBAR_HEIGHT})` }}
        >
            <div className="aside flex flex-col flex-1 items-end gap-2"></div>

            <div className="flex flex-col flex-2 max-h-full items-center ">
                <div className="flex flex-row items-center">
                    <div className="flex flex-col items-end gap-1">
                        <input
                            type="file"
                            accept="image/*"
                            id="imageInput"
                            onChange={handleImageUpload}
                            className="hidden"
                        />
                        <button
                            onClick={() => {
                                document.getElementById("imageInput")?.click();
                            }}
                            className="btn btn-circle  w-8 h-8 border-white border-2"
                        >
                            {<MdOutlineUploadFile />}
                        </button>
                        <button
                            onClick={() => {
                                setTool("eraser");
                            }}
                            className={`btn btn-circle  w-8 h-8 border-white border-2 ${tool === "eraser" ? "bg-black" : ""}`}
                        >
                            <BsFillEraserFill
                                className={
                                    tool === "eraser" ? "text-white" : ""
                                }
                            />
                        </button>

                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#ef4444");
                            }}
                            className="btn btn-circle w-8 h-8 size-2 bg-red-500 dark:bg-red-500 border-white border-2"
                        >
                            {tool === "pencil" && color === "#ef4444" ? (
                                <GoPencil className="stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>
                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#fb923c");
                            }}
                            className="btn btn-circle  w-8 h-8 bg-orange-400 dark:bg-orange-400 border-white border-2"
                        >
                            {tool === "pencil" && color === "#fb923c" ? (
                                <GoPencil className="stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>
                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#fcd34d");
                            }}
                            className="btn btn-circle  w-8 h-8 bg-yellow-300  border-white border-2"
                        >
                            {tool === "pencil" && color === "#fcd34d" ? (
                                <GoPencil className="stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>
                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#4ade80");
                            }}
                            className="btn btn-circle  w-8 h-8 bg-green-400 border-white border-2"
                        >
                            {tool === "pencil" && color === "#4ade80" ? (
                                <GoPencil className="stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>
                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#3b82f6");
                            }}
                            className="btn btn-circle  w-8 h-8 bg-blue-500 border-white border-2"
                        >
                            {tool === "pencil" && color === "#3b82f6" ? (
                                <GoPencil className="stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>
                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#8b5cf6");
                            }}
                            className="btn btn-circle w-8 h-8 bg-purple-500 border-white border-2"
                        >
                            {tool === "pencil" && color === "#8b5cf6" ? (
                                <GoPencil className="stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>
                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#ffffff");
                            }}
                            className="btn btn-circle  w-8 h-8 bg-white border-white border-2"
                        >
                            {tool === "pencil" && color === "#ffffff" ? (
                                <GoPencil className="stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>
                        <button
                            onClick={() => {
                                setTool("pencil");
                                setColor("#000000");
                            }}
                            className="btn btn-circle  w-8 h-8 bg-black border-white border-2"
                        >
                            {tool === "pencil" && color === "#000000" ? (
                                <GoPencil className="text-white stroke-2" />
                            ) : (
                                <p></p>
                            )}
                        </button>

                        <button
                            onClick={() =>
                                document.getElementById("colorPicker")?.click()
                            }
                            className="btn btn-circle  w-8 h-8 bg-gradient-to-r from-yellow-500 via-blue-500 to-purple-500 rainbow-animated"
                        ></button>
                        <div className="flex flex-col w-8 items-center gap-4">
                            <button
                                type="button"
                                className="btn btn-circle w-8 h-8  border-white border-2"
                                onClick={() => {
                                    setPencilThickness(pencilThickness - 1);
                                }}
                            >
                                -
                            </button>
                            <input
                                type="range"
                                id="thicknessSlider"
                                min="1"
                                max="20"
                                value={pencilThickness}
                                onChange={(e) =>
                                    setPencilThickness(Number(e.target.value))
                                }
                                className="range range-primary w-24 mt-6 mb-6"
                                style={{
                                    transform: "rotate(90deg)",
                                }}
                            />
                            <button
                                type="button"
                                className="btn btn-circle w-8 h-8  border-white border-2"
                                onClick={() => {
                                    setPencilThickness(pencilThickness + 1);
                                }}
                            >
                                +
                            </button>
                        </div>

                        <input
                            type="color"
                            id="colorPicker"
                            className="hidden"
                            onChange={(e) => {
                                setTool("pencil");
                                setColor(e.target.value);
                            }}
                        />
                    </div>

                    <div className="flex flex-col">
                        <div className="card h-fit w-fit border-base-200 border-1 bg-white shadow-md items-center justify-center ml-4 mr-4">
                            <canvas ref={canvasRef} id="canvas"></canvas>
                        </div>
                        <footer className="footer justify-items-end mt-2">
                            <form className="form" onSubmit={handleSubmit}>
                                <button
                                    type="submit"
                                    className="btn btn-primary mr-4"
                                >
                                    Publish
                                </button>
                            </form>
                        </footer>
                    </div>
                </div>
            </div>

            <div className="flex flex-1"></div>

            {/* Publish modal component */}
            <PublishPixelartModal
                imageUrl={imageUrl}
                isOpen={isModalOpen}
                onClose={handleCloseModal}
            />
        </div>
    );
}

export default CanvasPage;
