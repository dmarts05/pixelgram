import { JSX } from "react";
import Hero from "../components/Hero";
import Navbar from "../components/Navbar";

function LandingPage(): JSX.Element {
    return (
        <div className="min-h-screen">
            <Navbar />
            <Hero />
        </div>
    );
}

export default LandingPage;
