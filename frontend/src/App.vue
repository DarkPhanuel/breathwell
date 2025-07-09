<template>
  <div class="min-h-screen bg-gray-50">
    <div v-if="authState.loading" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <div class="w-16 h-16 border-4 border-blue-200 rounded-full animate-spin border-t-blue-600 mx-auto mb-4"></div>
        <p class="text-gray-600 text-lg">Chargement de SmartCity...</p>
      </div>
    </div>
    
    <div v-else-if="!authState.isAuthenticated">
      <LoginForm />
    </div>
    
    <div v-else class="min-h-screen">
      <TheHeader :active-tab="activeTab" @tab-change="activeTab = $event" />
      <main class="pt-28 p-6">
        <div class="max-w-7xl mx-auto">
          <component :is="currentView" />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import TheHeader from '@/components/TheHeader.vue'
import LoginForm from '@/components/LoginForm.vue'
import DashboardView from '@/components/DashboardView.vue'
import SettingsView from '@/components/SettingsView.vue'
import AdminView from '@/components/AdminView.vue'
import AlertsView from '@/components/AlertsView.vue'
import AnalyticsView from '@/components/AnalyticsView.vue'
import UsersView from '@/components/UsersView.vue'

const { authState, checkAuth } = useAuth()
const activeTab = ref('dashboard')

const currentView = computed(() => {
  switch (activeTab.value) {
    case 'dashboard':
      return DashboardView
    case 'alerts':
      return AlertsView
    case 'settings':
      return SettingsView
    case 'analytics':
      return AnalyticsView
    case 'users':
      return UsersView
    case 'admin':
      return AdminView
    default:
      return DashboardView
  }
})

onMounted(() => {
  checkAuth()
})
</script>