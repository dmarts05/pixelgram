import {
    InfiniteData,
    QueryObserverResult,
    RefetchOptions,
} from "@tanstack/react-query";
import { Post } from "../../types/post";
import { PostPage } from "../PostsGrid";
import PostCardActions from "./actions/PostCardActions";
import PostCardDescription from "./PostCardDescription";
import PostCardHeader from "./PostCardHeader";
import PostCardImage from "./PostCardImage";
import PostCardTimestamp from "./PostCardTimestamp";

const POST_CARD_IMAGE_SIZE = 256;

interface PostCardProps {
    post: Post;
    refetch: (
        options?: RefetchOptions
    ) => Promise<QueryObserverResult<InfiniteData<PostPage, unknown>, Error>>;
    showDeleteButton?: boolean;
}

function PostCard({
    post,
    refetch,
    showDeleteButton,
}: PostCardProps): React.ReactNode {
    return (
        <article
            className="card bg-base-100 shadow-md"
            style={{ minWidth: `${POST_CARD_IMAGE_SIZE}px` }}
        >
            <PostCardHeader
                authorUsername={post.authorUsername}
                authorId={post.userId}
            />
            <PostCardImage
                postId={post.id}
                imageUrl={post.imageUrl}
                imageAlt={post.description}
                height={POST_CARD_IMAGE_SIZE}
            />
            <div className="card-body">
                <PostCardActions
                    postId={post.id}
                    likesCount={post.likesCount}
                    likedByUser={post.likedByUser}
                    savedByUser={post.savedByUser}
                    commentsCount={post.commentsCount}
                    commentedByUser={post.commentedByUser}
                    refetch={refetch}
                    showDeleteButton={showDeleteButton}
                />
                <PostCardDescription description={post.description} />
                <PostCardTimestamp createdAt={post.createdAt} />
            </div>
        </article>
    );
}

export default PostCard;
