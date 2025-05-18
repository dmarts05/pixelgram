import React, { useEffect } from "react";

interface CanvasProps {
    canvasRef: React.RefObject<HTMLCanvasElement | null>;
    color: string;
    pencilThickness: number;
    tool: string;
    onPublish: () => void;
}

function Canvas({
    canvasRef,
    color,
    pencilThickness,
    tool,
    onPublish,
}: CanvasProps): React.ReactNode {
    const contextRef = React.useRef<CanvasRenderingContext2D | null>(null);

    const [cursor, setCursor] = React.useState<{x: number; y: number; visible: boolean}>({
        x: 0,
        y: 0,
        visible: false,
    });

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas?.getContext("2d");
        if (!canvas || !context) {
            return;
        }

        // Set canvas background color
        context.fillStyle = "rgba(0,0,0,1)";
        context.fillRect(0, 0, canvas.width, canvas.height);
        canvas.width = 128;
        canvas.height = 128;

        function resizeCanvas(): void {
            const size = Math.min(window.innerWidth, window.innerHeight) * 0.75;
            if (canvas && context) {
                canvas.style.width = `${size}px`;
                canvas.style.height = `${size}px`;

                context.imageSmoothingEnabled = false;

                // Store context to allow changing the color and tool
                contextRef.current = context;
            }
        }

        

        // Initial canvas size
        resizeCanvas();

        // Resize canvas on window resize
        window.addEventListener("resize", resizeCanvas);

        // Cleanup event listener on unmount
        return (): void => {
            window.removeEventListener("resize", resizeCanvas);
            
        };
    }, [canvasRef]);

    

    // Load tools and methods to draw on canvas when changing tool or color
    useEffect(() => {
        const canvas = canvasRef.current;
        const context = contextRef.current;
        if (!canvas || !context) {
            return;
        }

        let isDrawing = false;

        function getCanvasPosition(e: MouseEvent | TouchEvent): {
        x: number;
        y: number;
    } {
        const canvas = canvasRef.current;
        if (!canvas) {
            return { x: 0, y: 0 };
        }

        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width || 1;
        const scaleY = canvas.height / rect.height || 1;

        const processedEvent = e instanceof TouchEvent ? e.touches[0] : e;
        return {
            x: (processedEvent.clientX - rect.left) * scaleX || 1,
            y: (processedEvent.clientY - rect.top) * scaleY || 1,
        };
    }

    function draw(e: MouseEvent | TouchEvent, isDrawing: boolean): void {
        const context = contextRef.current;
        if (!context) {
            return;
        }
        if (!isDrawing) {
            return;
        }

        // Get x and y coordinates for the mouse or touch event
        const position = getCanvasPosition(e);
        const x = position.x;
        const y = position.y;

        // Draw on the canvas depending on the tool and color
        context.lineWidth = pencilThickness;
        context.lineCap = "round";
        context.strokeStyle = tool === "eraser" ? "rgba(0,0,0,1)" : color;
        context.globalCompositeOperation =
            tool === "eraser" ? "destination-out" : "source-over";
        context.lineTo(x, y);
        context.stroke();
        context.beginPath();
        context.moveTo(x, y);
    }

        function startDrawing(e: MouseEvent | TouchEvent): void {
            isDrawing = true;
            draw(e, isDrawing);
        }

        function stopDrawing(): void {
            isDrawing = false;
            context!.beginPath();
        }

        function updateCursor(e: MouseEvent | TouchEvent): void {
            
            let clientX: number, clientY: number;
            if (e instanceof TouchEvent) {
                if (e.touches.length === 0) return;
                clientX = e.touches[0].clientX;
                clientY = e.touches[0].clientY;
            } else {
                clientX = e.clientX;
                clientY = e.clientY;
            }
            if(canvas) {
                const rect = canvas.getBoundingClientRect();
                setCursor({
                    x: clientX - rect.left,
                    y: clientY - rect.top,
                    visible: true,
                });
            }   
        }

        function hideCursor():void {
            setCursor((c) => ({ ...c, visible: false }));
        }

        canvas.addEventListener("mouseleave", hideCursor);
        canvas.addEventListener("mouseenter", () => setCursor((c) => ({ ...c, visible: true })));
        canvas.addEventListener("touchmove", updateCursor);
        canvas.addEventListener("touchend", hideCursor);

        // Add event listeners for mouse and touch events
        canvas.addEventListener("mousedown", startDrawing);
        canvas.addEventListener("mouseup", stopDrawing);
        canvas.addEventListener("mousemove", (e) => {updateCursor(e); draw(e, isDrawing)});
        canvas.addEventListener("touchstart", (e) => {startDrawing(e)});
        canvas.addEventListener("touchend", () => {hideCursor(); stopDrawing()});
        canvas.addEventListener("touchmove", (e) => {updateCursor(e); draw(e, isDrawing)});

        // Cleanup event listeners on unmount
        return (): void => {
            canvas.removeEventListener("mouseleave", hideCursor);
            canvas.removeEventListener("mouseenter", () => setCursor((c) => ({ ...c, visible: true })));

            canvas.removeEventListener("mousedown", startDrawing);
            window.removeEventListener("mouseup", stopDrawing);
            canvas.removeEventListener("mousemove", (e) => {updateCursor(e); draw(e, isDrawing)});

            canvas.removeEventListener("touchstart", startDrawing);
            canvas.removeEventListener("touchend", () => {hideCursor(); stopDrawing()});
            canvas.removeEventListener("touchmove", (e) => {updateCursor(e); draw(e, isDrawing)});
        };
    }, [color, tool,pencilThickness, canvasRef]);
    return (
        <div className="flex flex-col gap-4">
            <div className="card bg-white shadow-md">
                <canvas ref={canvasRef}></canvas>
                {cursor.visible && tool === "pencil" && (
                    <div
                        style={{
                            position: "absolute",
                            pointerEvents: "none",
                            left: cursor.x - pencilThickness * 2,
                            top: cursor.y - pencilThickness * 2,
                            width: pencilThickness * 4,
                            height: pencilThickness * 4,
                            borderRadius: "50%",
                            border: `2px solid ${color}`,
                            background: "transparent",
                            zIndex: 10,
                            boxSizing: "border-box",
                        }}
                    />
                )}
            </div>
            <button
                className="btn btn-primary justify-items-end"
                onClick={onPublish}
            >
                Publish
            </button>
        </div>
    );
}

export default Canvas;
