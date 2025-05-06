import { create } from "zustand";

interface AuthState {
    userId: string | null;
    setUserId: (userId: string | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    userId: null,
    setUserId: (userId: string | null): void => {
        console.log("Setting userId:", userId);
        set({ userId });
    },
}));

export const useIsAuthenticated = (): boolean =>
    useAuthStore((state) => {
        console.log("isAuthenticated", state.userId);
        return state.userId !== null;
    });
