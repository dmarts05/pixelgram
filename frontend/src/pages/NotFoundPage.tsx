import { Link } from "react-router";

function NotFoundPage(): React.ReactNode {
    return (
        <div className="min-h-screen bg-base-200 flex items-center">
            <div className="text-center w-full">
                <h1 className="text-8xl font-bold">404</h1>
                <p className="my-6 text-2xl">
                    Oops! The page you're looking for doesn't exist.
                </p>
                <Link to="/">
                    <button className="btn btn-primary">Go Back to Home</button>
                </Link>
            </div>
        </div>
    );
}

export default NotFoundPage;
