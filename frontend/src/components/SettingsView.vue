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
            <span class="ml-2 text-sm font-medium text-gray-900">Paramètres du compte</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Header -->
    <div class="border-b border-gray-200 pb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Paramètres du compte</h1>
      <p class="text-gray-600">
        Gérez vos informations personnelles et vos préférences de notification.
      </p>
    </div>

    <!-- Profile Information -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <User class="w-5 h-5 mr-2" />
        Informations personnelles
      </h2>
      <form @submit.prevent="updateProfile" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Prénom <span class="text-red-500">*</span>
            </label>
            <input
              v-model="profileForm.firstName"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Nom <span class="text-red-500">*</span>
            </label>
            <input
              v-model="profileForm.lastName"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Adresse électronique <span class="text-red-500">*</span>
          </label>
          <input
            v-model="profileForm.email"
            type="email"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Numéro de téléphone
          </label>
          <input
            v-model="profileForm.phone"
            type="tel"
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="06 12 34 56 78"
          />
        </div>
        
        <button
          type="submit"
          :disabled="profileLoading"
          class="bg-blue-600 text-white py-3 px-6 rounded-sm font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ profileLoading ? 'Mise à jour en cours...' : 'Enregistrer les modifications' }}
        </button>
      </form>
    </div>

    <!-- Alert Settings -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <Bell class="w-5 h-5 mr-2" />
        Paramètres d'alertes
      </h2>
      
      <div class="space-y-6">
        <div class="flex items-start space-x-3">
          <input
            v-model="alertForm.emailAlertsEnabled"
            type="checkbox"
            class="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <div>
            <label class="text-gray-900 font-medium">Recevoir les alertes par courrier électronique</label>
            <p class="text-sm text-gray-600 mt-1">
              Vous recevrez une notification par email lorsque les seuils de pollution sont dépassés.
            </p>
          </div>
        </div>
        
        <div class="border-t border-gray-200 pt-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Seuils personnalisés d'alerte</h3>
          <p class="text-sm text-gray-600 mb-4">
            Définissez vos propres seuils d'alerte pour chaque polluant (en μg/m³).
          </p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Particules fines PM2.5
              </label>
              <input
                v-model.number="alertForm.alertThresholds.pm25"
                type="number"
                min="0"
                max="500"
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">Seuil réglementaire : 50 μg/m³</p>
            </div>
            
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Particules PM10
              </label>
              <input
                v-model.number="alertForm.alertThresholds.pm10"
                type="number"
                min="0"
                max="500"
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">Seuil réglementaire : 80 μg/m³</p>
            </div>
            
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Dioxyde d'azote NO2
              </label>
              <input
                v-model.number="alertForm.alertThresholds.no2"
                type="number"
                min="0"
                max="500"
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">Seuil réglementaire : 200 μg/m³</p>
            </div>
            
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                Ozone O3
              </label>
              <input
                v-model.number="alertForm.alertThresholds.o3"
                type="number"
                min="0"
                max="500"
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p class="text-xs text-gray-500 mt-1">Seuil réglementaire : 180 μg/m³</p>
            </div>
          </div>
        </div>
        
        <button
          @click="updateAlerts"
          :disabled="alertLoading"
          class="bg-blue-600 text-white py-3 px-6 rounded-sm font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ alertLoading ? 'Mise à jour en cours...' : 'Enregistrer les préférences' }}
        </button>
      </div>
    </div>

    <!-- Password Change -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <Lock class="w-5 h-5 mr-2" />
        Modification du mot de passe
      </h2>
      <form @submit.prevent="changePassword" class="space-y-6">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Mot de passe actuel <span class="text-red-500">*</span>
          </label>
          <input
            v-model="passwordForm.currentPassword"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Nouveau mot de passe <span class="text-red-500">*</span>
          </label>
          <input
            v-model="passwordForm.newPassword"
            type="password"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">
            Le mot de passe doit contenir au minimum 8 caractères.
          </p>
        </div>
        
        <button
          type="submit"
          :disabled="passwordLoading"
          class="bg-blue-600 text-white py-3 px-6 rounded-sm font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ passwordLoading ? 'Modification en cours...' : 'Modifier le mot de passe' }}
        </button>
      </form>
    </div>

    <!-- Legal Information -->
    <div class="bg-blue-50 rounded-sm border border-blue-200 p-6">
      <div class="flex items-start">
        <Info class="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
        <div>
          <h3 class="text-blue-900 font-semibold mb-2">Protection des données personnelles</h3>
          <p class="text-blue-800 text-sm leading-relaxed">
            Vos données personnelles sont traitées conformément au Règlement Général sur la Protection des Données (RGPD). 
            Vous disposez d'un droit d'accès, de rectification et de suppression de vos données. 
            Pour plus d'informations, consultez notre politique de confidentialité.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Home, ChevronRight, User, Bell, Lock, Info } from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'

const { authState, updateProfile: updateUserProfile, changePassword: changeUserPassword } = useAuth()

const profileLoading = ref(false)
const alertLoading = ref(false)
const passwordLoading = ref(false)

const profileForm = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: ''
})

const alertForm = reactive({
  emailAlertsEnabled: false,
  alertThresholds: {
    pm25: 50,
    pm10: 80,
    no2: 100,
    o3: 120
  }
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: ''
})

const updateProfile = async () => {
  profileLoading.value = true
  try {
    await updateUserProfile(profileForm)
  } catch (error) {
    console.error('Failed to update profile:', error)
  } finally {
    profileLoading.value = false
  }
}

const updateAlerts = async () => {
  alertLoading.value = true
  try {
    if (alertForm.alertThresholds) {
      await updateThreshold(alertForm.alertThresholds)
    }
    await updateUserProfile({ emailAlertsEnabled: alertForm.emailAlertsEnabled })
  } catch (error) {
    console.error('Failed to update alerts:', error)
  } finally {
    alertLoading.value = false
  }
}

const changePassword = async () => {
  passwordLoading.value = true
  try {
    await changeUserPassword(passwordForm.currentPassword, passwordForm.newPassword)
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
  } catch (error) {
    console.error('Failed to change password:', error)
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  if (authState.value.user) {
    profileForm.firstName = authState.value.user.firstName
    profileForm.lastName = authState.value.user.lastName
    profileForm.email = authState.value.user.email
    profileForm.phone = authState.value.user.phone || ''
    alertForm.emailAlertsEnabled = authState.value.user.emailAlertsEnabled
    alertForm.alertThresholds = { ...authState.value.user.alertThresholds }
  }
})
</script>