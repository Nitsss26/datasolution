import { create } from "zustand"
import { persist } from "zustand/middleware"
import axios from "axios"

interface User {
  id: string
  email: string
  company_name: string
  full_name: string
}

interface AuthStore {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (userData: {
    email: string
    password: string
    company_name: string
    full_name: string
  }) => Promise<void>
  logout: () => void
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
            email,
            password,
          })

          const { access_token, user } = response.data
          set({ user, token: access_token, isLoading: false })

          // Set default axios header
          axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (userData) => {
        set({ isLoading: true })
        try {
          const response = await axios.post(`${API_BASE_URL}/api/auth/register`, userData)

          const { access_token, user } = response.data
          set({ user, token: access_token, isLoading: false })

          // Set default axios header
          axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        set({ user: null, token: null })
        delete axios.defaults.headers.common["Authorization"]
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({ user: state.user, token: state.token }),
    },
  ),
)
