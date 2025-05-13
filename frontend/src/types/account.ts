export type AccountFormData = {
    username: string;
    email: string;
    password: string;
    confirmPassword: string;
};

export type Account = {
    id: string;
    username: string;
    email: string;
    isActive: boolean;
    isVerified: boolean;
    isSuperuser: boolean;
};

export type AccountPublicData = {
    id: string;
    username: string;
};
