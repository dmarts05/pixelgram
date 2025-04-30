import React, { JSX, useEffect, useState } from "react";
import { GoPencil } from "react-icons/go";
import {BsFillEraserFill} from "react-icons/bs";

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

                
                function startDrawing(e: MouseEvent):void {
                    drawing = true;
                    draw(e);
                    return;
                };

                function stopDrawing(e: MouseEvent):void {
                    drawing = false;
                    context.beginPath();
                };

                function draw(e: MouseEvent):void {
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
                
            }
            
        }
     }, []);

    return (
        <div className="flex flex-row">
            <div className="aside flex flex-col flex-1">
                <button onClick={() => {}} className="btn">Importar imagen</button>
                <button onClick={() => {setTool("eraser")}} className="btn btn-circle">{tool === "eraser" ? <BsFillEraserFill/> : <p></p>}</button>

                
                <button onClick={() => {setTool("pencil"); setColor("#ef4444")}} className="btn btn-circle bg-red-500">{tool === "pencil" && color === "#ef4444" ? <GoPencil/> : <p></p>}</button>
                <button onClick={() => {setTool("pencil"); setColor("#fb923c")}}className="btn btn-circle bg-orange-400">{tool === "pencil" && color === "#fb923c" ? <GoPencil/> : <p></p>}</button>
                <button onClick={() => {setTool("pencil"); setColor("#fcd34d")}} className="btn btn-circle bg-yellow-300">{tool === "pencil" && color === "#fcd34d" ? <GoPencil/> : <p></p>}</button>
                <button onClick={() => {setTool("pencil"); setColor("#4ade80")}} className="btn btn-circle bg-green-400">{tool === "pencil" && color === "#4ade80" ? <GoPencil/> : <p></p>}</button>
                <button onClick={() => {setTool("pencil"); setColor("#3b82f6")}} className="btn btn-circle bg-blue-500">{tool === "pencil" && color === "#3b82f6" ? <GoPencil/> : <p></p>}</button>
                <button onClick={() => {setTool("pencil"); setColor("#8b5cf6")}} className="btn btn-circle bg-purple-500">{tool === "pencil" && color === "#8b5cf6" ? <GoPencil/> : <p></p>}</button>
                <button onClick={() => {setTool("pencil"); setColor("#000000")}} className="btn btn-circle bg-black">{tool === "pencil" && color === "#000000" ? <GoPencil className="text-white"/> : <p></p>}</button>
                
                <button  className="btn btn-circle bg-gradient-to-r from-yellow-500 via-green-400 via-blue-500 to-purple-500 rainbow-animated"></button>

            </div>

            <div className="flex flex-col flex-2 max-h-full">
                <div className="canvas-container border-2">
                    <canvas id="canvas"></canvas>
                </div>

                <footer className="footer justify-items-center">
                    <form className="form" onSubmit={(e) =>{}}>
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