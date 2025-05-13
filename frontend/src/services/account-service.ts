import { Account, AccountPublicData } from "../types/account";
import { fetchApi } from "./fetch-api";

export type FetchAccountData = {
    password?: string;
    username?: string;
};

export async function updateUser({
    password,
    username,
}: FetchAccountData): Promise<Account> {
    const accountFetchData: FetchAccountData = {};
    if (password) {
        accountFetchData.password = password;
    }
    if (username) {
        accountFetchData.username = username;
    }

    const res = await fetchApi("users/me", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(accountFetchData),
    });

    if (!res.ok) {
        throw new Error("Failed to fetch posts");
    }

    return res.json();
}

export async function getMyUser(): Promise<Account> {
    const res = await fetchApi("users/me", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("Failed to fetch posts");
    }

    return res.json();
}

export async function getUsernameById(
    userId: string
): Promise<AccountPublicData> {
    const res = await fetchApi(`users/${userId}/info`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("Failed to fetch posts");
    }

    return res.json();
}
