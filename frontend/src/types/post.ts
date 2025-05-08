export type Post = {
    id: string;
    description: string;
    imageUrl: URL;
    userId: string;
    authorUsername: string;
    authorEmail: string;
    createdAt: Date;
    likesCount: number;
    likedByUser: boolean;
};
