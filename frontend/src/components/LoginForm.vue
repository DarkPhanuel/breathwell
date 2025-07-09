<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Bandeau République Française -->
    <div class="bg-blue-900 text-white py-1">
      <div class="max-w-7xl mx-auto px-6 flex items-center justify-between text-xs">
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
    </div>

    <div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <!-- Header -->
        <div class="text-center">
          <div class="mx-auto w-20 h-20 bg-blue-600 rounded-xl flex items-center justify-center mb-6">
            <span class="text-white text-3xl">🇫🇷</span>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">SmartCity Lyon</h1>
          <p class="text-gray-600">Système de surveillance de la qualité de l'air</p>
          <div class="mt-4 text-sm text-gray-500">
            <p>Service public de la Métropole de Lyon</p>
          </div>
        </div>

        <!-- Main Form Container -->
        <div class="bg-white rounded-sm shadow-md border border-gray-200 p-8">
          <!-- Mode Selection -->
          <div class="flex mb-6 bg-gray-100 rounded-sm p-1">
            <button
              @click="currentMode = 'login'"
              :class="[
                'flex-1 py-2 px-4 rounded-sm text-sm font-medium transition-colors',
                currentMode === 'login' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              Connexion
            </button>
            <button
              @click="currentMode = 'register'"
              :class="[
                'flex-1 py-2 px-4 rounded-sm text-sm font-medium transition-colors',
                currentMode === 'register' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              Inscription
            </button>
            <button
              @click="currentMode = 'reset'"
              :class="[
                'flex-1 py-2 px-4 rounded-sm text-sm font-medium transition-colors',
                currentMode === 'reset' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              Mot de passe
            </button>
          </div>

          <!-- Test Accounts Info -->
          <div v-if="currentMode === 'login'" class="mb-6 p-4 bg-blue-50 rounded-sm border border-blue-200">
            <p class="text-blue-800 text-sm font-semibold mb-2">Comptes de démonstration :</p>
            <div class="text-blue-700 text-xs space-y-1">
              <p><strong>Utilisateur :</strong> user@test.com / password123</p>
              <p><strong>Administrateur :</strong> admin@test.com / admin123</p>
            </div>
          </div>
          
          <!-- Login Form -->
          <form v-if="currentMode === 'login'" @submit.prevent="handleLogin" class="space-y-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Adresse électronique</label>
              <input
                v-model="loginForm.email"
                type="email"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="nom@exemple.fr"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Mot de passe</label>
              <input
                v-model="loginForm.password"
                type="password"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Votre mot de passe"
              />
            </div>

            <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-sm">
              <p class="text-red-700 text-sm">{{ error }}</p>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-blue-600 text-white py-3 px-4 rounded-sm font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {{ loading ? 'Connexion en cours...' : 'Se connecter' }}
            </button>
          </form>

          <!-- Register Form -->
          <form v-if="currentMode === 'register'" @submit.prevent="handleRegister" class="space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Prénom</label>
                <input
                  v-model="registerForm.firstName"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Prénom"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Nom</label>
                <input
                  v-model="registerForm.lastName"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Nom"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Adresse électronique</label>
              <input
                v-model="registerForm.email"
                type="email"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="nom@exemple.fr"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Numéro de téléphone</label>
              <input
                v-model="registerForm.phone"
                type="tel"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="06 12 34 56 78"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Mot de passe</label>
              <input
                v-model="registerForm.password"
                type="password"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Choisissez un mot de passe"
              />
            </div>

            <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-sm">
              <p class="text-red-700 text-sm">{{ error }}</p>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-blue-600 text-white py-3 px-4 rounded-sm font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {{ loading ? 'Inscription en cours...' : "Créer mon compte" }}
            </button>
          </form>

          <!-- Reset Password Form -->
          <form v-if="currentMode === 'reset'" @submit.prevent="handleResetPassword" class="space-y-6">
            <div class="text-center mb-4">
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Réinitialisation du mot de passe</h3>
              <p class="text-sm text-gray-600">Saisissez votre adresse électronique pour recevoir un lien de réinitialisation</p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Adresse électronique</label>
              <input
                v-model="resetForm.email"
                type="email"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="nom@exemple.fr"
              />
            </div>

            <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-sm">
              <p class="text-red-700 text-sm">{{ error }}</p>
            </div>
            
            <div v-if="resetSuccess" class="p-3 bg-green-50 border border-green-200 rounded-sm">
              <p class="text-green-700 text-sm">{{ resetSuccess }}</p>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full bg-blue-600 text-white py-3 px-4 rounded-sm font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {{ loading ? 'Envoi en cours...' : 'Envoyer le lien de réinitialisation' }}
            </button>
          </form>

          <!-- Footer -->
          <div class="mt-8 pt-6 border-t border-gray-200 text-center">
            <p class="text-xs text-gray-500">
              En vous connectant, vous acceptez les 
              <a href="#" class="text-blue-600 hover:underline">conditions d'utilisation</a> 
              et la 
              <a href="#" class="text-blue-600 hover:underline">politique de confidentialité</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuth } from '@/composables/useAuth'

const { login, register, resetPassword } = useAuth()

const currentMode = ref<'login' | 'register' | 'reset'>('login')
const loading = ref(false)
const error = ref('')
const resetSuccess = ref('')

const loginForm = reactive({
  email: '',
  password: ''
})

const registerForm = reactive({
  email: '',
  password: '',
  firstName: '',
  lastName: '',
  phone: ''
})

const resetForm = reactive({
  email: ''
})

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await login(loginForm.email, loginForm.password)
  } catch (err) {
    error.value = 'Identifiants invalides. Veuillez vérifier votre adresse électronique et votre mot de passe.'
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await register({
      email: registerForm.email,
      password: registerForm.password,
      firstName: registerForm.firstName,
      lastName: registerForm.lastName,
      phone: registerForm.phone,
      role: 'user',
      emailAlertsEnabled: true,
      alertThresholds: {
        pm25: 50,
        pm10: 80,
        no2: 100,
        o3: 120
      }
    })
  } catch (err) {
    error.value = "Échec de l'inscription. Veuillez réessayer."
  } finally {
    loading.value = false
  }
}

const handleResetPassword = async () => {
  loading.value = true
  error.value = ''
  resetSuccess.value = ''
  
  try {
    await resetPassword(resetForm.email)
    resetSuccess.value = 'Un lien de réinitialisation a été envoyé à votre adresse électronique.'
    resetForm.email = ''
  } catch (err) {
    error.value = 'Adresse électronique introuvable. Veuillez vérifier et réessayer.'
  } finally {
    loading.value = false
  }
}
</script>