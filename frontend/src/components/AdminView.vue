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
            <span class="ml-2 text-sm font-medium text-gray-900">Administration système</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Header -->
    <div class="border-b border-gray-200 pb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Administration système</h1>
      <p class="text-gray-600">
        Configuration et maintenance du système de surveillance de la qualité de l'air.
      </p>
    </div>

    <!-- Global Thresholds -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <Settings class="w-5 h-5 mr-2" />
        Seuils réglementaires globaux
      </h2>
      <p class="text-gray-600 text-sm mb-6">
        Configuration des seuils d'alerte conformément à la réglementation française sur la qualité de l'air.
      </p>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Seuil PM2.5 (μg/m³)
          </label>
          <input
            v-model.number="thresholds.pm25"
            type="number"
            min="0"
            max="500"
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">Valeur limite journalière : 25 μg/m³</p>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Seuil PM10 (μg/m³)
          </label>
          <input
            v-model.number="thresholds.pm10"
            type="number"
            min="0"
            max="500"
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">Valeur limite journalière : 50 μg/m³</p>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Seuil NO2 (μg/m³)
          </label>
          <input
            v-model.number="thresholds.no2"
            type="number"
            min="0"
            max="500"
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">Seuil d'alerte : 400 μg/m³ (moyenne horaire)</p>
        </div>
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Seuil O3 (μg/m³)
          </label>
          <input
            v-model.number="thresholds.o3"
            type="number"
            min="0"
            max="500"
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">Seuil d'alerte : 240 μg/m³ (moyenne horaire)</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Seuil ATMO global
          </label>
          <input
            v-model.number="thresholds.atmo"
            type="number"
            min="0"
            max="10"
            step="0.1"
            class="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p class="text-xs text-gray-500 mt-1">Indice ATMO : 1 (très bon) à 10 (très mauvais)</p>
        </div>
      </div>
      
      <button
        @click="updateThresholds"
        :disabled="thresholdsLoading"
        class="mt-6 bg-blue-600 text-white py-3 px-6 rounded-sm font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {{ thresholdsLoading ? 'Mise à jour en cours...' : 'Enregistrer les seuils' }}
      </button>
    </div>

    <!-- ATMO Configuration -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <BarChart3 class="w-5 h-5 mr-2" />
        Configuration de l'indice ATMO
      </h2>
      <p class="text-gray-600 text-sm mb-6">
        L'indice ATMO caractérise la qualité de l'air quotidienne d'une agglomération. 
        Il est calculé à partir des concentrations de plusieurs polluants.
      </p>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <h3 class="font-semibold text-gray-900">Échelle ATMO</h3>
          <div class="space-y-2">
            <div class="flex items-center justify-between p-3 bg-green-50 rounded-sm border border-green-200">
              <span class="font-medium text-green-800">1-2 : Très bon</span>
              <span class="text-green-600 text-sm">Aucune restriction</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-yellow-50 rounded-sm border border-yellow-200">
              <span class="font-medium text-yellow-800">3-4 : Bon</span>
              <span class="text-yellow-600 text-sm">Activités normales</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-orange-50 rounded-sm border border-orange-200">
              <span class="font-medium text-orange-800">5-6 : Moyen</span>
              <span class="text-orange-600 text-sm">Personnes sensibles</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-red-50 rounded-sm border border-red-200">
              <span class="font-medium text-red-800">7-8 : Médiocre</span>
              <span class="text-red-600 text-sm">Réduire les activités</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-purple-50 rounded-sm border border-purple-200">
              <span class="font-medium text-purple-800">9-10 : Mauvais</span>
              <span class="text-purple-600 text-sm">Éviter les sorties</span>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <h3 class="font-semibold text-gray-900">Paramètres de calcul</h3>
          <div class="space-y-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Pondération PM2.5
              </label>
              <input
                v-model.number="atmoConfig.pm25Weight"
                type="number"
                min="0"
                max="1"
                step="0.1"
                class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Pondération PM10
              </label>
              <input
                v-model.number="atmoConfig.pm10Weight"
                type="number"
                min="0"
                max="1"
                step="0.1"
                class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Pondération NO2
              </label>
              <input
                v-model.number="atmoConfig.no2Weight"
                type="number"
                min="0"
                max="1"
                step="0.1"
                class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Pondération O3
              </label>
              <input
                v-model.number="atmoConfig.o3Weight"
                type="number"
                min="0"
                max="1"
                step="0.1"
                class="w-full px-3 py-2 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      </div>

      <button
        @click="updateAtmoConfig"
        :disabled="atmoLoading"
        class="mt-6 bg-green-600 text-white py-3 px-6 rounded-sm font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {{ atmoLoading ? 'Mise à jour en cours...' : 'Enregistrer la configuration ATMO' }}
      </button>
    </div>

    <!-- System Management -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Data Management -->
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <Database class="w-5 h-5 mr-2" />
          Gestion des données
        </h2>
        <p class="text-gray-600 text-sm mb-6">
          Maintenance et archivage des données de mesure de la qualité de l'air.
        </p>
        
        <div class="space-y-4">
          <button
            @click="clearData"
            :disabled="clearLoading"
            class="w-full bg-red-600 text-white py-3 px-4 rounded-sm font-semibold hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ clearLoading ? 'Suppression en cours...' : 'Purger les données anciennes' }}
          </button>
          
          <div class="p-4 bg-yellow-50 rounded-sm border border-yellow-200">
            <div class="flex items-start">
              <AlertTriangle class="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
              <div>
                <p class="text-yellow-800 text-sm font-medium">Attention</p>
                <p class="text-yellow-700 text-sm mt-1">
                  Cette action supprimera définitivement les données de plus de 2 ans. 
                  L'opération ne peut pas être annulée.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Model Training -->
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <Brain class="w-5 h-5 mr-2" />
          Modèle de prédiction
        </h2>
        <p class="text-gray-600 text-sm mb-6">
          Ré-entraînement du modèle d'intelligence artificielle pour améliorer la précision des prévisions.
        </p>
        
        <div class="space-y-4">
          <button
            @click="trainModel"
            :disabled="trainLoading"
            class="w-full bg-green-600 text-white py-3 px-4 rounded-sm font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ trainLoading ? 'Entraînement en cours...' : 'Lancer l\'entraînement' }}
          </button>
          
          <div class="p-4 bg-blue-50 rounded-sm border border-blue-200">
            <div class="flex items-start">
              <Info class="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
              <div>
                <p class="text-blue-800 text-sm font-medium">Information</p>
                <p class="text-blue-700 text-sm mt-1">
                  L'entraînement utilise les données des 12 derniers mois. 
                  Durée estimée : 15-30 minutes.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- System Status -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
        <Activity class="w-5 h-5 mr-2" />
        État du système
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="text-center p-4 bg-green-50 rounded-sm border border-green-200">
          <div class="text-3xl font-bold text-green-600 mb-2">24/24</div>
          <p class="text-green-800 text-sm font-medium">Capteurs actifs</p>
          <p class="text-green-600 text-xs mt-1">Fonctionnement normal</p>
        </div>
        
        <div class="text-center p-4 bg-blue-50 rounded-sm border border-blue-200">
          <div class="text-3xl font-bold text-blue-600 mb-2">94.2%</div>
          <p class="text-blue-800 text-sm font-medium">Précision IA</p>
          <p class="text-blue-600 text-xs mt-1">Modèle performant</p>
        </div>
        
        <div class="text-center p-4 bg-purple-50 rounded-sm border border-purple-200">
          <div class="text-3xl font-bold text-purple-600 mb-2">2min</div>
          <p class="text-purple-800 text-sm font-medium">Dernière MAJ</p>
          <p class="text-purple-600 text-xs mt-1">Données récentes</p>
        </div>
        
        <div class="text-center p-4 bg-orange-50 rounded-sm border border-orange-200">
          <div class="text-3xl font-bold text-orange-600 mb-2">99.8%</div>
          <p class="text-orange-800 text-sm font-medium">Disponibilité</p>
          <p class="text-orange-600 text-xs mt-1">Service stable</p>
        </div>
      </div>
    </div>

    <!-- Legal Notice -->
    <div class="bg-blue-50 rounded-sm border border-blue-200 p-6">
      <div class="flex items-start">
        <Info class="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
        <div>
          <h3 class="text-blue-900 font-semibold mb-2">Cadre réglementaire</h3>
          <p class="text-blue-800 text-sm leading-relaxed">
            Ce système est conforme à la directive européenne 2008/50/CE et au Code de l'environnement français. 
            Les mesures sont effectuées selon les méthodes de référence définies par l'INERIS et validées par le LCSQA.
            L'indice ATMO est calculé conformément à l'arrêté du 22 juillet 2004.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Home, ChevronRight, Settings, Database, Brain, Activity, AlertTriangle, Info, BarChart3 } from 'lucide-vue-next'
import { adminAPI } from '@/services/api'

const thresholdsLoading = ref(false)
const clearLoading = ref(false)
const trainLoading = ref(false)
const atmoLoading = ref(false)

const thresholds = reactive({
  pm25: 35,
  pm10: 50,
  no2: 80,
  o3: 100,
  atmo: 6.0
})

const atmoConfig = reactive({
  pm25Weight: 0.3,
  pm10Weight: 0.25,
  no2Weight: 0.25,
  o3Weight: 0.2
})

const updateThresholds = async () => {
  thresholdsLoading.value = true
  try {
    await adminAPI.updateGlobalThresholds(thresholds)
  } catch (error) {
    console.error('Failed to update thresholds:', error)
  } finally {
    thresholdsLoading.value = false
  }
}

const updateAtmoConfig = async () => {
  atmoLoading.value = true
  try {
    await adminAPI.updateAtmoConfig(atmoConfig)
  } catch (error) {
    console.error('Failed to update ATMO config:', error)
  } finally {
    atmoLoading.value = false
  }
}

const clearData = async () => {
  if (confirm('Êtes-vous sûr de vouloir purger les données anciennes ? Cette action ne peut pas être annulée.')) {
    clearLoading.value = true
    try {
      await adminAPI.clearData()
    } catch (error) {
      console.error('Failed to clear data:', error)
    } finally {
      clearLoading.value = false
    }
  }
}

const trainModel = async () => {
  trainLoading.value = true
  try {
    await adminAPI.trainModel()
  } catch (error) {
    console.error('Failed to train model:', error)
  } finally {
    trainLoading.value = false
  }
}

onMounted(async () => {
  try {
    const globalThresholds = await adminAPI.getGlobalThresholds()
    Object.assign(thresholds, globalThresholds)
  } catch (error) {
    console.error('Failed to fetch thresholds:', error)
  }
})
</script>