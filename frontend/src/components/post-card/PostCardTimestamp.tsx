import { formatDistanceToNow } from "date-fns";

type PostCardTimestampProps = {
    createdAt: Date;
    color?: string;
    uppercase?: boolean;
};

function PostCardTimestamp({
    createdAt,
    color = "text-base-content/60",
    uppercase = true,
}: PostCardTimestampProps): React.ReactNode {
    const timeAgo = formatDistanceToNow(new Date(createdAt), {
        addSuffix: true,
    });

    return (
        <p className={`text-xs ${color} ${uppercase ? "uppercase" : ""}`}>
            {timeAgo}
        </p>
    );
}

export default PostCardTimestamp;
