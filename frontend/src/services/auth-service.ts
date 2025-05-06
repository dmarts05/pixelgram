import { LogInFormData } from "../components/forms/LogInForm";
import { AccountFormData } from "../components/forms/SignUpForm";
import { fetchApi } from "./fetch-api";

export async function signUp(data: AccountFormData): Promise<void> {
    const response = await fetchApi("auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        switch (response.status) {
            case 400:
                throw new Error("Another user with this email already exists.");
            case 422:
                throw new Error("Invalid data provided.");
            default:
                throw new Error("Unexpected error trying to sign up");
        }
    }
}

export async function logIn(data: LogInFormData): Promise<void> {
    const formData = new FormData();
    formData.append("username", data.email);
    formData.append("password", data.password);

    const response = await fetchApi("auth/login", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        switch (response.status) {
            case 400:
                throw new Error("Invalid email or password.");
            case 422:
                throw new Error("Invalid data provided.");
            default:
                throw new Error("Unexpected error trying to log in");
        }
    }
}

export async function authGoogle(): Promise<void> {
    const response = await fetchApi("auth/google/authorize");

    if (!response.ok) {
        switch (response.status) {
            case 422:
                throw new Error("Invalid data provided.");
            default:
                throw new Error(
                    "Unexpected error trying to authorize with Google"
                );
        }
    }

    const data = await response.json();
    window.location.href = data.authorization_url;
}

export async function authGoogleCallback(query: string): Promise<void> {
    const response = await fetchApi(`auth/google/callback${query}`);
    if (!response.ok) {
        switch (response.status) {
            case 400:
                throw new Error("Invalid state token.");
            case 422:
                throw new Error("Invalid data provided.");
            default:
                throw new Error(
                    "Unexpected error trying to authorize with Google"
                );
        }
    }
}

export async function logout(): Promise<void> {
    const response = await fetchApi("auth/logout", {
        method: "POST",
    });

    if (!response.ok) {
        switch (response.status) {
            case 401:
                throw new Error("You are not logged in.");
            default:
                throw new Error("Unexpected error trying to log out");
        }
    }
}

export async function getUserId(): Promise<string | null> {
    const response = await fetchApi("users/me", {
        method: "GET",
    });

    if (!response.ok) {
        return null;
    }

    const data = await response.json();
    return data.id;
}
