<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm">
    <!-- Bandeau République Française avec Navigation -->
    <div class="bg-blue-900 text-white">
      <div class="max-w-7xl mx-auto px-6">
        <!-- Première ligne: République Française et liens officiels -->
        <div class="flex items-center justify-between text-xs py-1 border-b border-blue-800">
          <div class="flex items-center space-x-4">
            <span class="font-medium">République Française</span>
            <span class="text-blue-200">|</span>
            <span>Liberté • Égalité • Fraternité</span>
          </div>
          <div class="flex items-center space-x-4">
            <span>service-public.fr</span>
            <span class="text-blue-200">|</span>
            <span>legifrance.gouv.fr</span>
          </div>
        </div>
        
        <!-- Navigation principale -->
        <nav class="flex items-center justify-between py-2">
          <div class="flex items-center space-x-8">
            <button
              v-for="item in menuItems"
              :key="item.id"
              @click="$emit('tab-change', item.id)"
              :class="[
                'flex items-center space-x-2 px-3 py-2 text-sm font-medium transition-colors rounded-sm',
                activeTab === item.id
                  ? 'text-white bg-blue-800'
                  : 'text-blue-100 hover:text-white hover:bg-blue-800'
              ]"
            >
              <component :is="item.icon" class="w-4 h-4" />
              <span>{{ item.label }}</span>
            </button>
          </div>
          
          <!-- Menu utilisateur simplifié -->
          <div class="relative">
            <button
              @click="showDropdown = !showDropdown"
              class="flex items-center space-x-2 px-3 py-2 text-blue-100 hover:text-white hover:bg-blue-800 rounded-sm transition-colors text-sm"
            >
              <div class="w-6 h-6 bg-blue-700 rounded-sm flex items-center justify-center">
                <span class="text-white font-medium text-xs">
                  {{ authState.user?.email?.charAt(0) }}{{ authState.user?.email?.charAt(1) }}
                </span>
              </div>
              <span>{{ authState.user?.email }}</span>
              <ChevronDown class="w-3 h-3" />
            </button>

            <Transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="opacity-0 scale-95 translate-y-1"
              enter-to-class="opacity-100 scale-100 translate-y-0"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="opacity-100 scale-100 translate-y-0"
              leave-to-class="opacity-0 scale-95 translate-y-1"
            >
              <div v-if="showDropdown" class="absolute right-0 mt-2 w-48 bg-white rounded-sm shadow-lg py-1 z-50 border border-gray-200">
                <div class="px-4 py-2 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-900">{{ authState.user?.email }}</p>
                  <p class="text-xs text-gray-500">{{ authState.user?.is_admin === true ? 'Administrateur' : 'Utilisateur' }}</p>
                </div>
                
                <button
                  @click="handleLogout"
                  class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center space-x-2 transition-colors text-sm"
                >
                  <LogOut class="w-4 h-4" />
                  <span>Déconnexion</span>
                </button>
              </div>
            </Transition>
          </div>
        </nav>
      </div>
    </div>

    <!-- Header principal -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <!-- Logo Marianne -->
            <div class="w-12 h-12 bg-blue-600 rounded-sm flex items-center justify-center">
              <span class="text-white font-bold text-lg">🇫🇷</span>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">SmartCity Lyon</h1>
              <p class="text-sm text-gray-600">Surveillance de la qualité de l'air</p>
            </div>
          </div>

          <div class="flex items-center space-x-4">
            <!-- Notifications -->
            <div class="relative">
              <button class="p-2 text-gray-600 hover:bg-gray-100 rounded-sm transition-colors relative">
                <Bell class="w-5 h-5" />
                <div class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-sm flex items-center justify-center">
                  <span class="text-xs font-bold text-white">3</span>
                </div>
              </button>
            </div>
            
            <!-- Statut système -->
            <div class="flex items-center space-x-2 text-sm text-gray-500">
              <div class="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Système opérationnel</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Bell, LogOut, ChevronDown, Home, AlertTriangle, Settings, BarChart3, Users, Shield } from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'

defineProps<{
  activeTab: string
}>()

defineEmits<{
  'tab-change': [tab: string]
}>()

const { authState, logout } = useAuth()
const showDropdown = ref(false)

const menuItems = computed(() => [
  { id: 'dashboard', label: 'Tableau de bord', icon: Home },
  { id: 'alerts', label: 'Alertes', icon: AlertTriangle },
  { id: 'settings', label: 'Paramètres', icon: Settings },
  ...(authState.value.user?.is_admin === true ? [
    { id: 'analytics', label: 'Analyses', icon: BarChart3 },
    { id: 'users', label: 'Utilisateurs', icon: Users },
    { id: 'admin', label: 'Administration', icon: Shield }
  ] : [])
])

const handleLogout = async () => {
  try {
    await logout()
    showDropdown.value = false
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>