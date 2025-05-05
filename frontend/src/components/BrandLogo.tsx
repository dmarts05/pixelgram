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
    enableLinkToHomeLogo?: boolean;
    enableLinkToHomeText?: boolean;
};

function BrandLogo({
    text = "Pixelgram",
    width: widthValue = 40,
    height: heightValue = 40,
    textSize = "xl",
    direction = "row",
    enableLinkToHomeLogo = true,
    enableLinkToHomeText = false,
}: BrandLogoProps): React.ReactNode {
    const navigate = useNavigate();

    const enableBothLinks = enableLinkToHomeLogo && enableLinkToHomeText;

    return (
        <div
            className={`flex items-center justify-center gap-2 ${
                direction === "column" ? "flex-col" : "flex-row"
            } ${enableBothLinks && "cursor-pointer"}`}
            onClick={() => {
                if (enableBothLinks) {
                    navigate("/");
                }
            }}
        >
            <img
                src={logoImg}
                alt="Pixelgram Logo"
                className={`${enableLinkToHomeLogo && "cursor-pointer"}`}
                onClick={() => {
                    if (enableLinkToHomeLogo) {
                        navigate("/");
                    }
                }}
                width={widthValue}
                height={heightValue}
            />
            <h2
                className={`text-${textSize} font-bold select-none ${
                    enableLinkToHomeText && "cursor-pointer"
                }`}
                onClick={() => {
                    if (enableLinkToHomeText) {
                        navigate("/");
                    }
                }}
            >
                {text}
            </h2>
        </div>
    );
}

export default BrandLogo;
