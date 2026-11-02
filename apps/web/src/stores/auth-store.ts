import { create } from "zustand";
import { UserRole, UserProfile } from "@brandkotha/api-client";

interface AuthState {
  token: string | null;
  role: UserRole | null;
  user: UserProfile | null;
  isAuthenticated: boolean;
  setAuth: (token: string, role: UserRole, user: UserProfile) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  role: null,
  user: null,
  isAuthenticated: false,
  setAuth: (token, role, user) => set({ token, role, user, isAuthenticated: true }),
  logout: () => set({ token: null, role: null, user: null, isAuthenticated: false }),
}));

