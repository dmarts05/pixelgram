import { Post } from "../../types/post";
import PostCardActions from "./PostCardActions";
import PostCardDescription from "./PostCardDescription";
import PostCardHeader from "./PostCardHeader";
import PostCardImage from "./PostCardImage";
import PostCardTimestamp from "./PostCardTimestamp";

const POST_CARD_IMAGE_SIZE = 256;

type PostCardProps = {
    post: Post;
};

function PostCard({ post }: PostCardProps): React.ReactNode {
    return (
        <article
            className="card bg-base-100 shadow-md"
            style={{ minWidth: `${POST_CARD_IMAGE_SIZE}px` }}
        >
            <PostCardHeader authorUsername={post.authorUsername} />
            <PostCardImage
                imageUrl={post.imageUrl}
                imageAlt={post.description}
                height={POST_CARD_IMAGE_SIZE}
            />
            <div className="card-body">
                <PostCardActions
                    onLike={() => console.log("Like")}
                    onComment={() => console.log("Comment")}
                    onBookmark={() => console.log("Bookmark")}
                />
                <PostCardDescription description={post.description} />
                <PostCardTimestamp createdAt={post.createdAt} />
            </div>
        </article>
    );
}

export default PostCard;
