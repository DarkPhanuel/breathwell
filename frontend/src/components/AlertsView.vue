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
            <span class="ml-2 text-sm font-medium text-gray-900">Alertes pollution</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Header -->
    <div class="border-b border-gray-200 pb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Alertes pollution</h1>
      <p class="text-gray-600 max-w-3xl">
        Surveillance des dépassements de seuils réglementaires de qualité de l'air. 
        Les alertes sont déclenchées selon les critères définis par le Code de l'environnement.
      </p>
    </div>

    <!-- Alert Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Alertes actives</p>
            <p class="text-3xl font-bold text-red-600">{{ criticalAlerts }}</p>
            <p class="text-xs text-gray-500 mt-1">Niveau critique</p>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
            <AlertTriangle class="w-6 h-6 text-red-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Avertissements</p>
            <p class="text-3xl font-bold text-orange-600">{{ warningAlerts }}</p>
            <p class="text-xs text-gray-500 mt-1">Seuil d'information</p>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <AlertCircle class="w-6 h-6 text-orange-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Informations</p>
            <p class="text-3xl font-bold text-blue-600">{{ infoAlerts }}</p>
            <p class="text-xs text-gray-500 mt-1">Surveillance renforcée</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <Info class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-600 text-sm font-medium">Zones conformes</p>
            <p class="text-3xl font-bold text-green-600">{{ healthyZones }}</p>
            <p class="text-xs text-gray-500 mt-1">Qualité satisfaisante</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <CheckCircle class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Filtres</h2>
      <div class="flex flex-wrap items-center gap-4">
        <div class="flex items-center space-x-2">
          <label class="text-gray-700 text-sm font-medium">Type d'alerte :</label>
          <select v-model="selectedType" class="border border-gray-300 rounded-sm px-3 py-2 text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="all">Toutes les alertes</option>
            <option value="critical">Alertes critiques</option>
            <option value="warning">Avertissements</option>
            <option value="info">Informations</option>
          </select>
        </div>
        
        <div class="flex items-center space-x-2">
          <label class="text-gray-700 text-sm font-medium">Polluant :</label>
          <select v-model="selectedPollutant" class="border border-gray-300 rounded-sm px-3 py-2 text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="all">Tous les polluants</option>
            <option value="PM2.5">Particules fines PM2.5</option>
            <option value="PM10">Particules PM10</option>
            <option value="NO2">Dioxyde d'azote NO2</option>
            <option value="O3">Ozone O3</option>
          </select>
        </div>

        <button 
          @click="refreshAlerts"
          class="bg-blue-600 text-white px-4 py-2 rounded-sm text-sm font-medium hover:bg-blue-700 transition-colors"
        >
          Actualiser
        </button>
      </div>
    </div>

    <!-- Alerts List -->
    <div class="space-y-4">
      <h2 class="text-lg font-semibold text-gray-900">Alertes en cours</h2>
      
      <div 
        v-for="alert in filteredAlerts" 
        :key="alert.id"
        :class="[
          'bg-white rounded-sm shadow-sm border p-6 hover:shadow-md transition-shadow',
          getAlertBorderColor(alert.type)
        ]"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-4">
            <div :class="[
              'w-12 h-12 rounded-sm flex items-center justify-center',
              getAlertBgColor(alert.type)
            ]">
              <component :is="getAlertIcon(alert.type)" class="w-6 h-6 text-white" />
            </div>
            
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h3 class="text-gray-900 font-semibold text-lg">{{ alert.message }}</h3>
                <span :class="[
                  'px-3 py-1 rounded-sm text-xs font-medium',
                  getAlertTypeStyle(alert.type)
                ]">
                  {{ getAlertTypeText(alert.type) }}
                </span>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600 mb-4">
                <div>
                  <span class="font-medium">Polluant :</span>
                  <span class="ml-1">{{ alert.pollutant }}</span>
                </div>
                <div>
                  <span class="font-medium">Concentration :</span>
                  <span class="ml-1 font-semibold">{{ alert.value }} μg/m³</span>
                </div>
                <div>
                  <span class="font-medium">Seuil réglementaire :</span>
                  <span class="ml-1">{{ alert.threshold }} μg/m³</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4 text-sm text-gray-500">
                  <div class="flex items-center space-x-1">
                    <MapPin class="w-4 h-4" />
                    <span>{{ alert.location }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <Clock class="w-4 h-4" />
                    <span>{{ formatTime(alert.timestamp) }}</span>
                  </div>
                </div>
                
                <div class="flex space-x-2">
                  <button class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-sm text-xs font-medium transition-colors">
                    Voir détails
                  </button>
                  <button class="bg-blue-100 hover:bg-blue-200 text-blue-700 px-3 py-1 rounded-sm text-xs font-medium transition-colors">
                    Marquer comme lu
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredAlerts.length === 0" class="text-center py-12 bg-white rounded-sm shadow-sm border border-gray-200">
      <div class="w-16 h-16 bg-green-100 rounded-sm flex items-center justify-center mx-auto mb-4">
        <CheckCircle class="w-8 h-8 text-green-600" />
      </div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">Aucune alerte active</h3>
      <p class="text-gray-600">La qualité de l'air respecte actuellement les seuils réglementaires</p>
    </div>

    <!-- Information Panel -->
    <div class="bg-blue-50 rounded-sm border border-blue-200 p-6">
      <div class="flex items-start">
        <Info class="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
        <div>
          <h3 class="text-blue-900 font-semibold mb-2">Information réglementaire</h3>
          <p class="text-blue-800 text-sm leading-relaxed">
            Les seuils d'alerte sont définis par l'arrêté du 7 avril 2016 relatif aux modalités de surveillance 
            de la qualité de l'air et aux informations à transmettre au public. Les mesures sont effectuées 
            conformément aux normes européennes en vigueur.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Home, ChevronRight, AlertTriangle, AlertCircle, Info, CheckCircle, MapPin, Clock } from 'lucide-vue-next'
import { pollutionAPI } from '@/services/api'

const alerts = ref<any[]>([])
const selectedType = ref('all')
const selectedPollutant = ref('all')

const criticalAlerts = computed(() => alerts.value.filter(a => a.type === 'critical').length)
const warningAlerts = computed(() => alerts.value.filter(a => a.type === 'warning').length)
const infoAlerts = computed(() => alerts.value.filter(a => a.type === 'info').length)
const healthyZones = computed(() => 12)

const filteredAlerts = computed(() => {
  return alerts.value.filter(alert => {
    const typeMatch = selectedType.value === 'all' || alert.type === selectedType.value
    const pollutantMatch = selectedPollutant.value === 'all' || alert.pollutant === selectedPollutant.value
    return typeMatch && pollutantMatch
  })
})

const getAlertIcon = (type: string) => {
  switch (type) {
    case 'critical': return AlertTriangle
    case 'warning': return AlertCircle
    case 'info': return Info
    default: return AlertCircle
  }
}

const getAlertBorderColor = (type: string): string => {
  switch (type) {
    case 'critical': return 'border-red-200'
    case 'warning': return 'border-orange-200'
    case 'info': return 'border-blue-200'
    default: return 'border-gray-200'
  }
}

const getAlertBgColor = (type: string): string => {
  switch (type) {
    case 'critical': return 'bg-red-500'
    case 'warning': return 'bg-orange-500'
    case 'info': return 'bg-blue-500'
    default: return 'bg-gray-500'
  }
}

const getAlertTypeStyle = (type: string): string => {
  switch (type) {
    case 'critical': return 'bg-red-100 text-red-800 border border-red-200'
    case 'warning': return 'bg-orange-100 text-orange-800 border border-orange-200'
    case 'info': return 'bg-blue-100 text-blue-800 border border-blue-200'
    default: return 'bg-gray-100 text-gray-800 border border-gray-200'
  }
}

const getAlertTypeText = (type: string): string => {
  switch (type) {
    case 'critical': return 'ALERTE'
    case 'warning': return 'AVERTISSEMENT'
    case 'info': return 'INFORMATION'
    default: return 'NOTIFICATION'
  }
}

const formatTime = (timestamp: string): string => {
  const date = new Date(timestamp)
  return date.toLocaleString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const refreshAlerts = async () => {
  try {
    alerts.value = await pollutionAPI.getAlerts()
  } catch (error) {
    console.error('Failed to refresh alerts:', error)
  }
}

onMounted(async () => {
  await refreshAlerts()
})
</script>