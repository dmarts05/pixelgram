import React, { useEffect, useState } from "react";

function CanvasPage() {

    const [tool, setTool] = useState<"pencil" | "eraser">("pencil");
    const [color, setColor] = useState<string>("#000000");

    return (
        <div className="flex flex-row">
            <div className="aside flex flex-col flex-2">
                <button className="btn btn-primary">Borrar</button>
                <button className="btn btn-primary">Lápiz</button>
                
                
                <button className="btn btn-circle border-b-neutral-50 bg-red-500"></button>
                <button className="btn btn-circle bg-orange-400"></button>
                <button className="btn btn-circle bg-yellow-300"></button>
                <button className="btn btn-circle bg-green-400"></button>
                <button className="btn btn-circle bg-blue-500"></button>
                <button className="btn btn-circle bg-purple-500"></button>
                <button className="btn btn-circle bg-black"></button>
                
                <button className="btn btn-circle bg-gradient-to-r from-yellow-500 via-green-400 via-blue-500 to-purple-500 rainbow-animated"></button>

                

            </div>

            <div className="flex flex-1">
                <div className="canvas-container border-2">
                    <canvas id="canvas" width="800" height="800"></canvas>
                </div>

            </div>

        </div>
    );
}

export default CanvasPage;