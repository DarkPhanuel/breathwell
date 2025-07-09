import { ref, computed } from 'vue'
import type { User, AuthState, AlertThreshold } from '@/types'
import { authAPI } from '@/services/api'

const authState = ref<AuthState>({
  user: null,
  isAuthenticated: false,
  loading: true
})

export const useAuth = () => {
  const login = async (email: string, password: string) => {
    authState.value.loading = true
    try {
      const user = await authAPI.login(email, password)
      authState.value = {
        user,
        isAuthenticated: true,
        loading: false
      }
    } catch (error) {
      authState.value = {
        user: null,
        isAuthenticated: false,
        loading: false
      }
      throw error
    }
  }

  const register = async (userData: Omit<User, 'id' | 'createdAt'>) => {
    authState.value.loading = true
    try {
      // Le mot de passe sera passé depuis le formulaire d'inscription
      const user = await authAPI.register(userData as any)
      authState.value = {
        user,
        isAuthenticated: true,
        loading: false
      }
    } catch (error) {
      authState.value = {
        user: null,
        isAuthenticated: false,
        loading: false
      }
      throw error
    }
  }

  const resetPassword = async (email: string) => {
    await authAPI.resetPassword(email)
  }

  const logout = async () => {
    authState.value.loading = true
    try {
      await authAPI.logout()
      authState.value = {
        user: null,
        isAuthenticated: false,
        loading: false
      }
    } catch (error) {
      authState.value = {
        user: null,
        isAuthenticated: false,
        loading: false
      }
      throw error
    }
  }

  const changePassword = async (currentPassword: string, newPassword: string) => {
    await authAPI.changePassword(currentPassword, newPassword)
  }

  const updateProfile = async (updates: Partial<User>) => {
    if (!authState.value.user) return
    
    authState.value.loading = true
    try {
      const updatedUser = await authAPI.updateProfile(updates)
      authState.value = {
        user: updatedUser,
        isAuthenticated: true,
        loading: false
      }
    } catch (error) {
      authState.value.loading = false
      throw error
    }
  }

  const updateThreshold = async (thresholds: AlertThreshold) => {
    await authAPI.updateThreshold(thresholds)
    if (authState.value.user) {
      authState.value.user.alertThresholds = thresholds
    }
  }
  const checkAuth = async () => {
    try {
      const user = await authAPI.getCurrentUser()
      authState.value = {
        user,
        isAuthenticated: !!user,
        loading: false
      }
    } catch (error) {
      authState.value = {
        user: null,
        isAuthenticated: false,
        loading: false
      }
    }
  }

  return {
    authState: computed(() => authState.value),
    login,
    register,
    resetPassword,
    logout,
    changePassword,
    updateProfile,
    updateThreshold,
    checkAuth
  }
}