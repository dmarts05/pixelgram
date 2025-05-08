export type PostComment = {
    id: string;
    postId: string;
    userId: string;
    authorUsername: string;
    authorEmail: string;
    content: string;
    createdAt: Date;
    byUser: boolean;
};
