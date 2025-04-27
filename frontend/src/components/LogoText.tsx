import { JSX } from "react";
import logoImg from "../assets/inverted-pixelgram-logo.webp";

function LogoText(): JSX.Element {
    return (
        <div className="flex items-center gap-2">
            <img src={logoImg} alt="Pixelgram Logo" className="w-10 h-10" />
            <div className="text-xl font-bold">Pixelgram</div>
        </div>
    );
}

export default LogoText;
