import { LogInFormData } from "../components/LogInForm";
import { SignUpFormData } from "../components/SignUpForm";
import { API_URL } from "../utils/constants";

export async function signUp(data: SignUpFormData): Promise<void> {
    const response = await fetch(`${API_URL}/auth/register`, {
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

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        body: formData,
        credentials: "include",
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

export async function logout(): Promise<void> {
    const response = await fetch(`${API_URL}/auth/logout`, {
        method: "POST",
        credentials: "include",
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
