<template>
  <aside class="fixed left-0 top-20 w-64 h-full bg-white border-r border-gray-200 z-40">
    <nav class="p-4 space-y-1">
      <button
        v-for="item in menuItems"
        :key="item.id"
        @click="$emit('tab-change', item.id)"
        :class="[
          'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors text-left font-medium',
          activeTab === item.id
            ? 'bg-blue-50 text-blue-700 border-l-4 border-blue-600'
            : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
        ]"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <span>{{ item.label }}</span>
      </button>
    </nav>

    <!-- System Status -->
    <div class="absolute bottom-4 left-4 right-4">
      <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <h3 class="text-gray-900 font-semibold text-sm mb-3 flex items-center">
          <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
          État du système
        </h3>
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-600">Capteurs actifs</span>
            <span class="text-green-600 font-semibold">24/24</span>
          </div>
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-600">Dernière MAJ</span>
            <span class="text-blue-600 font-semibold">2min</span>
          </div>
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-600">Précision IA</span>
            <span class="text-purple-600 font-semibold">94.2%</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Home, Settings, Users, AlertTriangle, BarChart3, Shield } from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'

defineProps<{
  activeTab: string
}>()

defineEmits<{
  'tab-change': [tab: string]
}>()

const { authState } = useAuth()

const menuItems = computed(() => [
  { id: 'dashboard', label: 'Tableau de bord', icon: Home },
  { id: 'alerts', label: 'Alertes', icon: AlertTriangle },
  { id: 'settings', label: 'Paramètres', icon: Settings },
  ...(authState.value.user?.role === 'admin' ? [
    { id: 'analytics', label: 'Analyses', icon: BarChart3 },
    { id: 'users', label: 'Utilisateurs', icon: Users },
    { id: 'admin', label: 'Administration', icon: Shield }
  ] : [])
])
</script>