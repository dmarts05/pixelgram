import React, { JSX, useEffect, useState } from "react";
import { GoPencil } from "react-icons/go";
import {BsFillEraserFill} from "react-icons/bs";
import {MdOutlineUploadFile} from "react-icons/md";

function CanvasPage(): JSX.Element {

    const [tool, setTool] = useState<"pencil" | "eraser">("pencil");
    const [color, setColor] = useState<string>("#000000");

    const canvasRef = React.useRef<HTMLCanvasElement | null>(null);
    const contextRef = React.useRef<CanvasRenderingContext2D | null>(null);


    useEffect(() => {
        const canvas = canvasRef.current;
        if(canvas) {
            const context = canvas.getContext("2d");
            if (context) {
                canvas.width = 128;
                canvas.height = 128;

                canvas.style.width = "512px";
                canvas.style.height = "512px";

                context.imageSmoothingEnabled = false;

                // Set canvas background color
                context.fillStyle = "#ffffff";
                context.fillRect(0, 0, canvas.width, canvas.height);

                // Store the context to allow changing the color and tool
                contextRef.current = context;
            }
        }
    }, []);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = contextRef.current;
        if(canvas && context) {
            let drawing = false;

            function draw(e: MouseEvent):void {
                if (!drawing) return;

                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;   // relationship bitmap vs. element for X
                const scaleY = canvas.height / rect.height; // relationship bitmap vs. element for Y
                const x = (e.clientX - rect.left) * scaleX;
                const y = (e.clientY - rect.top) * scaleY;



                context.lineWidth = 5;
                context.lineCap = "round";
                context.strokeStyle = tool === "eraser" ? "#ffffff" : color;

                context.lineTo(x, y);
                context.stroke();
                context.beginPath();
                context.moveTo(x, y);
            };

                function startDrawing(e: MouseEvent):void {
                    drawing = true;
                    draw(e);
                };

                function stopDrawing(e: MouseEvent):void {
                    drawing = false;
                    context.beginPath();
                };

                canvas.addEventListener("mousedown", startDrawing);
                canvas.addEventListener("mouseup", stopDrawing);
                canvas.addEventListener("mousemove", draw);

                return () => {
                    canvas.removeEventListener("mousedown", startDrawing);
                    canvas.removeEventListener("mouseup", stopDrawing);
                    canvas.removeEventListener("mousemove", draw);
                };
                
                
            
            
        }
    }, [color, tool]);

    function handleImageUpload(e:React.ChangeEvent<HTMLInputElement>):void {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.src = event.target?.result as string;
                img.onload = () => {
                    const canvas = document.getElementById("canvas") as HTMLCanvasElement;
                    if (canvas) {
                        const context = canvas.getContext("2d");
                        if (context) {
                            context.drawImage(img, 0, 0, canvas.width, canvas.height);
                        }
                    }
                };
                if(reader.result) {
                    img.src = reader.result as string;
                }
            };
            reader.readAsDataURL(file);
        }
        return;

    }


    function handleSubmit(e:React.FormEvent<HTMLFormElement>):void {
        e.preventDefault();
    }

    return (
        <div className="flex flex-row">
            <div className="aside flex flex-col flex-1">
                <input type="file" accept="image/*" id="imageInput" onChange={handleImageUpload} className="hidden"/>
                <button onClick={() => {document.getElementById("imageInput")?.click()}} className="btn btn-circle">{<MdOutlineUploadFile/>}</button>
                <button onClick={() => {setTool("eraser")}} className={`btn btn-circle ${tool === "eraser" ? "bg-black" : ""}`}><BsFillEraserFill className={tool === "eraser" ? "text-white" : ""}/></button>

                
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
                    <canvas ref={canvasRef} id="canvas"></canvas>
                </div>

                <footer className="footer justify-items-center">
                    <form className="form" onSubmit={handleSubmit}>
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