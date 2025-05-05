type PostCardHeaderProps = {
    authorUsername: string;
};

function PostCardHeader({
    authorUsername,
}: PostCardHeaderProps): React.ReactNode {
    return (
        <div className="py-2 px-4">
            <span className="font-semibold text-sm">{authorUsername}</span>
        </div>
    );
}

export default PostCardHeader;
