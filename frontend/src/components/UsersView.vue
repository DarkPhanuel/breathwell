<template>
  <div class="space-y-8">
    <!-- Breadcrumb -->
    <nav class="flex" aria-label="Breadcrumb">
      <ol class="flex items-center space-x-4">
        <li>
          <div class="flex items-center">
            <Home class="w-4 h-4 text-gray-400" />
            <span class="ml-2 text-sm font-medium text-gray-500">Accueil</span>
          </div>
        </li>
        <li>
          <div class="flex items-center">
            <ChevronRight class="w-4 h-4 text-gray-400" />
            <span class="ml-2 text-sm font-medium text-gray-900">Gestion des utilisateurs</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Header -->
    <div class="border-b border-gray-200 pb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Gestion des utilisateurs</h1>
      <p class="text-gray-600">
        Administration des comptes utilisateurs et gestion des permissions d'accès.
      </p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Total utilisateurs</p>
            <p class="text-3xl font-bold text-gray-900">{{ users.length }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">👥</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Utilisateurs actifs</p>
            <p class="text-3xl font-bold text-gray-900">{{ activeUsers }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">✅</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Administrateurs</p>
            <p class="text-3xl font-bold text-gray-900">{{ adminUsers }}</p>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">👑</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Alertes activées</p>
            <p class="text-3xl font-bold text-gray-900">{{ alertsEnabled }}</p>
          </div>
          <div class="w-12 h-12 bg-gray-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">🔔</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Actions -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6 mb-8">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <label class="text-gray-700 text-sm font-medium">Rôle:</label>
            <select v-model="selectedRole" class="border border-gray-300 rounded-sm px-3 py-2 text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="all">Tous</option>
              <option value="user">Utilisateur</option>
              <option value="admin">Administrateur</option>
            </select>
          </div>
          
          <div class="flex items-center space-x-2">
            <label class="text-gray-700 text-sm font-medium">Alertes:</label>
            <select v-model="selectedAlerts" class="border border-gray-300 rounded-sm px-3 py-2 text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="all">Tous</option>
              <option value="enabled">Activées</option>
              <option value="disabled">Désactivées</option>
            </select>
          </div>
        </div>

        <button 
          @click="showAddUser = true"
          class="bg-blue-600 text-white px-4 py-2 rounded-sm text-sm font-medium hover:bg-blue-700 transition-colors"
        >
          Ajouter utilisateur
        </button>
      </div>
    </div>

    <!-- Users Table -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left py-4 px-6 text-gray-700 font-medium">Utilisateur</th>
              <th class="text-left py-4 px-6 text-gray-700 font-medium">Contact</th>
              <th class="text-left py-4 px-6 text-gray-700 font-medium">Rôle</th>
              <th class="text-left py-4 px-6 text-gray-700 font-medium">Alertes</th>
              <th class="text-left py-4 px-6 text-gray-700 font-medium">Inscription</th>
              <th class="text-left py-4 px-6 text-gray-700 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="user in filteredUsers" 
              :key="user.id"
              class="border-b border-gray-100 hover:bg-gray-50 transition-colors duration-200"
            >
              <td class="py-4 px-6">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-blue-600 rounded-sm flex items-center justify-center">
                    <span class="text-white font-bold text-sm">
                      {{ user.firstName.charAt(0) }}{{ user.lastName.charAt(0) }}
                    </span>
                  </div>
                  <div>
                    <p class="text-gray-900 font-medium">{{ user.firstName }} {{ user.lastName }}</p>
                    <p class="text-gray-500 text-sm">{{ user.email }}</p>
                  </div>
                </div>
              </td>
              <td class="py-4 px-6">
                <p class="text-gray-700 text-sm">{{ user.phone }}</p>
              </td>
              <td class="py-4 px-6">
                <span :class="[
                  'px-3 py-1 rounded-sm text-xs font-medium',
                  user.role === 'admin' 
                    ? 'bg-red-100 text-red-800 border border-red-200'
                    : 'bg-blue-100 text-blue-800 border border-blue-200'
                ]">
                  {{ user.role === 'admin' ? 'Administrateur' : 'Utilisateur' }}
                </span>
              </td>
              <td class="py-4 px-6">
                <span :class="[
                  'px-3 py-1 rounded-sm text-xs font-medium',
                  user.emailAlertsEnabled 
                    ? 'bg-green-100 text-green-800 border border-green-200'
                    : 'bg-gray-100 text-gray-800 border border-gray-200'
                ]">
                  {{ user.emailAlertsEnabled ? 'Activées' : 'Désactivées' }}
                </span>
              </td>
              <td class="py-4 px-6">
                <p class="text-gray-700 text-sm">{{ formatDate(user.createdAt) }}</p>
              </td>
              <td class="py-4 px-6">
                <div class="flex space-x-2">
                  <button 
                    @click="editUser(user)"
                    class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-sm text-xs transition-colors"
                  >
                    Modifier
                  </button>
                  <button 
                    @click="deleteUser(user.id)"
                    class="bg-red-100 hover:bg-red-200 text-red-700 px-3 py-1 rounded-sm text-xs transition-colors"
                  >
                    Supprimer
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add User Modal -->
    <div v-if="showAddUser" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-sm shadow-lg border border-gray-200 max-w-md w-full mx-4 p-6">
        <h3 class="text-2xl font-bold text-gray-900 mb-6">Ajouter un utilisateur</h3>
        
        <form @submit.prevent="addUser" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Prénom</label>
              <input
                v-model="newUser.firstName"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nom</label>
              <input
                v-model="newUser.lastName"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              v-model="newUser.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
            <input
              v-model="newUser.phone"
              type="tel"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Rôle</label>
            <select
              v-model="newUser.role"
              class="w-full px-3 py-2 border border-gray-300 rounded-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="user">Utilisateur</option>
              <option value="admin">Administrateur</option>
            </select>
          </div>
          
          <div class="flex items-center space-x-3">
            <input
              v-model="newUser.emailAlertsEnabled"
              type="checkbox"
              class="w-4 h-4 text-blue-600 border-gray-300 rounded-sm focus:ring-blue-500"
            />
            <label class="text-gray-700">Activer les alertes email</label>
          </div>
          
          <div class="flex space-x-3 pt-4">
            <button
              type="submit"
              class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-sm font-medium hover:bg-blue-700 transition-colors"
            >
              Ajouter
            </button>
            <button
              type="button"
              @click="showAddUser = false"
              class="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-sm font-medium hover:bg-gray-200 transition-colors"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Information Panel -->
    <div class="bg-blue-50 rounded-sm border border-blue-200 p-6">
      <div class="flex items-start">
        <Info class="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
        <div>
          <h3 class="text-blue-900 font-semibold mb-2">Gestion des données personnelles</h3>
          <p class="text-blue-800 text-sm leading-relaxed">
            La gestion des utilisateurs respecte le Règlement Général sur la Protection des Données (RGPD). 
            Tous les utilisateurs disposent d'un droit d'accès, de rectification et de suppression de leurs données personnelles.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Home, ChevronRight, Info } from 'lucide-vue-next'
import { adminAPI } from '@/services/api'
import type { User } from '@/types'

const users = ref<User[]>([])
const selectedRole = ref('all')
const selectedAlerts = ref('all')
const showAddUser = ref(false)

const newUser = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  role: 'user' as 'user' | 'admin',
  emailAlertsEnabled: true
})

const activeUsers = computed(() => users.value.length)
const adminUsers = computed(() => users.value.filter(u => u.role === 'admin').length)
const alertsEnabled = computed(() => users.value.filter(u => u.emailAlertsEnabled).length)

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const roleMatch = selectedRole.value === 'all' || user.role === selectedRole.value
    const alertsMatch = selectedAlerts.value === 'all' || 
      (selectedAlerts.value === 'enabled' && user.emailAlertsEnabled) ||
      (selectedAlerts.value === 'disabled' && !user.emailAlertsEnabled)
    return roleMatch && alertsMatch
  })
})

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR')
}

const addUser = () => {
  const user: User = {
    id: Date.now().toString(),
    ...newUser.value,
    alertThresholds: {
      pm25: 50,
      pm10: 80,
      no2: 100,
      o3: 120
    },
    createdAt: new Date().toISOString()
  }
  
  users.value.push(user)
  showAddUser.value = false
  
  // Reset form
  newUser.value = {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    role: 'user',
    emailAlertsEnabled: true
  }
}

const editUser = (user: User) => {
  // Implementation for editing user
  console.log('Edit user:', user)
}

const deleteUser = (userId: string) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
    users.value = users.value.filter(u => u.id !== userId)
  }
}

onMounted(async () => {
  try {
    const fetchedUsers = await adminAPI.getUsers()
    users.value = fetchedUsers
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
})
</script>