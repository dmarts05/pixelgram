import React, { JSX, useEffect, useState } from "react";

function CanvasPage(): JSX.Element {

    const [tool, setTool] = useState<"pencil" | "eraser">("pencil");
    const [color, setColor] = useState<string>("#000000");


    useEffect(() => {
        const canvas = document.getElementById("canvas") as HTMLCanvasElement;
        if(canvas) {
            
            const context = canvas.getContext("2d");
            if (context) {
                canvas.width = 128;
                canvas.height = 128;

                canvas.style.width = "512px";
                canvas.style.height = "512px";

                context.imageSmoothingEnabled = false;

                context.fillStyle = color;
                context.fillRect(0, 0, canvas.width, canvas.height);

                let drawing = false;

                /*
                function startDrawing(e: MouseEvent) {
                    drawing = true;
                    draw(e);
                };

                function stopDrawing(e: MouseEvent) {
                    drawing = false;
                    context.beginPath();
                };

                function draw(e: MouseEvent) {
                    if (!drawing) return;
                    context.lineWidth = 5;
                    context.lineCap = "round";
                    context.strokeStyle = color;

                    context.lineTo(e.clientX, e.clientY);
                    context.stroke();
                    context.beginPath();
                    context.moveTo(e.clientX, e.clientY);
                };

                canvas.addEventListener("mousedown", startDrawing);
                canvas.addEventListener("mouseup", stopDrawing);
                canvas.addEventListener("mousemove", draw);
                */
            }
            
        }
     }, []);

    return (
        <div className="flex flex-row">
            <div className="aside flex flex-col flex-1">
                <button onClick={() => {setTool("eraser")}} className="btn btn-circle">Borrar</button>

                
                <button onClick={() => {setColor("#ef4444")}} className="btn btn-circle bg-red-500"></button>
                <button onClick={() => {setColor("#fb923c")}}className="btn btn-circle bg-orange-400"></button>
                <button onClick={() => {setColor("#fcd34d")}} className="btn btn-circle bg-yellow-300"></button>
                <button onClick={() => {setColor("#4ade80")}} className="btn btn-circle bg-green-400"></button>
                <button onClick={() => {setColor("#3b82f6")}} className="btn btn-circle bg-blue-500"></button>
                <button onClick={() => {setColor("#8b5cf6")}} className="btn btn-circle bg-purple-500"></button>
                <button onClick={() => {setColor("#000000")}} className="btn btn-circle bg-black"></button>
                
                <button  className="btn btn-circle bg-gradient-to-r from-yellow-500 via-green-400 via-blue-500 to-purple-500 rainbow-animated"></button>

            </div>

            <div className="flex flex-col flex-2 max-h-full">
                <div className="canvas-container border-2">
                    <canvas id="canvas"></canvas>
                </div>

                <footer className="footer justify-items-center">
                    <form className="form">
                        <button type="submit" className="btn btn-primary">Publicar</button>
                    </form>
                </footer>

            </div>

            <div className="flex flex-1">

            </div>

        </div>
    );
}

export default CanvasPage;