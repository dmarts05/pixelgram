import { Link } from "react-router";

type PostCardHeaderProps = {
    authorUsername: string;
    authorId: string;
    authorName: string;
};

function PostCardHeader({
    authorUsername,
    authorId,
}: PostCardHeaderProps): React.ReactNode {
    return (
        <div className="py-2 px-4">
            <span className="font-semibold text-sm">
                <Link to={`/users/${authorId}`} className="link link-hover">
                    {authorUsername}
                </Link>
            </span>
        </div>
    );
}

export default PostCardHeader;
