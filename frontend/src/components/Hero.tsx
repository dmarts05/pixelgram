import { Link } from "react-router";
import heroImg from "../assets/hero.webp";
import { NAVBAR_HEIGHT } from "../utils/constants";

function Hero(): React.ReactNode {
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
                    <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-4">
                        Welcome to Pixelgram
                    </h1>
                    <p className="mb-6 text-lg md:text-xl lg:text-2xl">
                        Share and discover beautiful pixel art with the world.
                    </p>
                    <Link to="/auth/signup" className="btn btn-primary">
                        Get Started
                    </Link>
                </div>
            </div>
        </section>
    );
}

export default Hero;
