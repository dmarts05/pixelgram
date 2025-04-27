import { JSX } from "react";
import { useNavigate } from "react-router";
import logoImg from "../assets/inverted-pixelgram-logo.webp";

type BrandLogoProps = {
    text?: string;
    width?: number;
    height?: number;
    textSize?:
        | "xs"
        | "sm"
        | "base"
        | "lg"
        | "xl"
        | "2xl"
        | "3xl"
        | "4xl"
        | "5xl"
        | "6xl"
        | "7xl"
        | "8xl"
        | "9xl";
    direction?: "row" | "column";
};

function BrandLogo({
    text = "Pixelgram",
    width: widthValue = 40,
    height: heightValue = 40,
    textSize = "xl",
    direction = "row",
}: BrandLogoProps): JSX.Element {
    const navigate = useNavigate();

    return (
        <div
            className={`flex items-center justify-center gap-2 ${
                direction === "column" ? "flex-col" : "flex-row"
            }`}
        >
            <img
                src={logoImg}
                alt="Pixelgram Logo"
                className="cursor-pointer"
                onClick={() => navigate("/")}
                width={widthValue}
                height={heightValue}
            />
            <h2 className={`text-${textSize} font-bold select-none`}>{text}</h2>
        </div>
    );
}

export default BrandLogo;
