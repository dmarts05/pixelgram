import { JSX } from "react";
import heroImg from "../assets/hero.webp";
import { NAVBAR_HEIGHT } from "../utils/constants";

function Hero(): JSX.Element {
    return (
        <section
            className="hero bg-cover bg-center"
            style={{
                backgroundImage: `url(${heroImg})`,
                height: `calc(100vh - ${NAVBAR_HEIGHT})`,
            }}
        >
            <div className="hero-overlay"></div>
            <div className="hero-content text-center text-white">
                <div>
                    <h1 className="text-5xl font-bold mb-4">
                        Welcome to Pixelgram
                    </h1>
                    <p className="mb-6 text-lg">
                        Share and discover beautiful pixel art with the world.
                    </p>
                    <button className="btn btn-primary">Get Started</button>
                </div>
            </div>
        </section>
    );
}

export default Hero;
