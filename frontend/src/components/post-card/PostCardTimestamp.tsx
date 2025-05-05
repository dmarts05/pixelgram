import { formatDistanceToNow } from "date-fns";

type PostCardTimestampProps = {
    createdAt: Date;
};

function PostCardTimestamp({
    createdAt,
}: PostCardTimestampProps): React.ReactNode {
    const timeAgo = formatDistanceToNow(new Date(createdAt), {
        addSuffix: true,
    });

    return <p className="text-xs text-base-content/60 uppercase">{timeAgo}</p>;
}

export default PostCardTimestamp;
