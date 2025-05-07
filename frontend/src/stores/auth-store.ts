import { create } from "zustand";

interface AuthState {
    userId: string | null;
    setUserId: (userId: string | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    userId: null,
    setUserId: (userId: string | null): void => {
        set({ userId });
    },
}));

export const useIsAuthenticated = (): boolean =>
    useAuthStore((state) => {
        return state.userId !== null;
    });
