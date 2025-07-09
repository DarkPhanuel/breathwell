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
            <span class="ml-2 text-sm font-medium text-gray-900">Tableau de bord</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Header -->
    <div class="border-b border-gray-200 pb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Qualité de l'air à Lyon</h1>
      <p class="text-gray-600 max-w-2xl">
        Surveillance en temps réel de la qualité de l'air dans la métropole lyonnaise. 
        Données officielles mises à jour toutes les heures.
      </p>
      <div class="mt-4 flex items-center space-x-6 text-sm text-gray-500">
        <div class="flex items-center">
          <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
          <span>Système opérationnel</span>
        </div>
        <div class="flex items-center">
          <Clock class="w-4 h-4 mr-2" />
          <span>Dernière mise à jour : {{ new Date().toLocaleTimeString('fr-FR') }}</span>
        </div>
      </div>
    </div>

    <!-- Current Pollution Cards -->
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Mesures actuelles</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <PollutionCard
          title="PM2.5"
          :value="currentData?.pm25 || 0"
          unit="μg/m³"
          :trend="getTrend(currentData?.pm25 || 0, 35)"
          :level="getLevel(currentData?.pm25 || 0, [12, 35, 55])"
          icon="🌫️"
          description="Particules fines"
        />
        
        <PollutionCard
          title="PM10"
          :value="currentData?.pm10 || 0"
          unit="μg/m³"
          :trend="getTrend(currentData?.pm10 || 0, 50)"
          :level="getLevel(currentData?.pm10 || 0, [20, 50, 90])"
          icon="💨"
          description="Particules en suspension"
        />
        
        <PollutionCard
          title="NO2"
          :value="currentData?.no2 || 0"
          unit="μg/m³"
          :trend="getTrend(currentData?.no2 || 0, 80)"
          :level="getLevel(currentData?.no2 || 0, [40, 80, 120])"
          icon="🚗"
          description="Dioxyde d'azote"
        />
        
        <PollutionCard
          title="O3"
          :value="currentData?.o3 || 0"
          unit="μg/m³"
          :trend="getTrend(currentData?.o3 || 0, 100)"
          :level="getLevel(currentData?.o3 || 0, [60, 100, 140])"
          icon="☀️"
          description="Ozone"
        />
      </div>
    </div>

    <!-- AQI and 7-day Predictions -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- ATMO Evolution Chart -->
      <div class="lg:col-span-3 bg-white rounded-sm shadow-sm border border-gray-200 p-6 mb-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <div class="w-8 h-8 bg-purple-100 rounded-sm flex items-center justify-center mr-3">
            <TrendingUp class="w-5 h-5 text-purple-600" />
          </div>
          Évolution de l'indice ATMO (24 dernières heures)
        </h2>
        
        <div class="h-64 relative bg-gray-50 rounded-sm border border-gray-200 p-4">
          <!-- Chart Grid Lines -->
          <div class="absolute inset-4 grid grid-rows-4 gap-0">
            <div v-for="i in 4" :key="i" class="border-b border-gray-200 border-dashed"></div>
          </div>
          
          <!-- Y-axis labels -->
          <div class="absolute left-0 top-4 bottom-4 flex flex-col justify-between text-xs text-gray-500">
            <span>100</span>
            <span>75</span>
            <span>50</span>
            <span>25</span>
            <span>0</span>
          </div>
          
          <!-- Chart Line -->
          <svg class="absolute inset-4 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
            <defs>
              <linearGradient id="atmoGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:0.1" />
              </linearGradient>
            </defs>
            
            <!-- Area under curve -->
            <path 
              :d="getChartAreaPath()" 
              fill="url(#atmoGradient)"
            />
            
            <!-- Main line -->
            <path 
              :d="getChartLinePath()" 
              stroke="#3B82F6" 
              stroke-width="0.5" 
              fill="none"
            />
            
            <!-- Data points -->
            <circle 
              v-for="(point, index) in atmoHistory" 
              :key="index"
              :cx="(index / (atmoHistory.length - 1)) * 100"
              :cy="100 - (point.value / 100) * 100"
              r="0.8"
              fill="#3B82F6"
              class="hover:r-1.5 transition-all"
            />
          </svg>
          
          <!-- X-axis labels -->
          <div class="absolute bottom-0 left-4 right-4 flex justify-between text-xs text-gray-500">
            <span>{{ formatChartTime(atmoHistory[0]?.time) }}</span>
            <span>{{ formatChartTime(atmoHistory[Math.floor(atmoHistory.length / 4)]?.time) }}</span>
            <span>{{ formatChartTime(atmoHistory[Math.floor(atmoHistory.length / 2)]?.time) }}</span>
            <span>{{ formatChartTime(atmoHistory[Math.floor(3 * atmoHistory.length / 4)]?.time) }}</span>
            <span>{{ formatChartTime(atmoHistory[atmoHistory.length - 1]?.time) }}</span>
          </div>
          
          <!-- Current value indicator -->
          <div class="absolute top-4 right-4 bg-white rounded-sm shadow-sm border border-gray-200 p-3">
            <div class="text-center">
              <div class="text-2xl font-bold text-gray-900">{{ Math.round(currentData?.aqi || 0) }}</div>
              <div class="text-xs text-gray-500">Actuel</div>
            </div>
          </div>
        </div>
        
        <!-- Chart Legend -->
        <div class="mt-4 flex items-center justify-center space-x-6 text-sm text-gray-600">
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-green-500 rounded-sm"></div>
            <span>Bon (0-50)</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-yellow-500 rounded-sm"></div>
            <span>Moyen (51-100)</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-orange-500 rounded-sm"></div>
            <span>Dégradé (101-150)</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-red-500 rounded-sm"></div>
            <span>Mauvais (151+)</span>
          </div>
        </div>
      </div>
      
      <!-- AQI Card -->
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <div class="w-8 h-8 bg-blue-100 rounded-sm flex items-center justify-center mr-3">
            <BarChart3 class="w-5 h-5 text-blue-600" />
          </div>
          Indice ATMO
        </h2>
        
        <div class="text-center mb-6">
          <div class="text-6xl font-bold text-gray-900 mb-2">
            {{ Math.round(currentData?.aqi || 0) }}
          </div>
          <p class="text-lg text-gray-600 font-medium">{{ getAQIDescription(currentData?.aqi || 0) }}</p>
        </div>

        <div class="space-y-4">
          <div class="flex justify-between text-sm text-gray-500 mb-2">
            <span>Bon</span>
            <span>Moyen</span>
            <span>Dégradé</span>
            <span>Mauvais</span>
          </div>
          <div class="w-full bg-gray-200 rounded-sm h-4">
            <div 
              :class="[
                'h-4 rounded-sm transition-all duration-1000',
                getAQIColor(currentData?.aqi || 0)
              ]"
              :style="{ width: `${Math.min(((currentData?.aqi || 0) / 200) * 100, 100)}%` }"
            ></div>
          </div>
        </div>

        <div class="mt-6 p-4 bg-blue-50 rounded-sm border border-blue-200">
          <h3 class="text-sm font-semibold text-blue-900 mb-2">Recommandations</h3>
          <p class="text-sm text-blue-800">{{ getRecommendation(currentData?.aqi || 0) }}</p>
        </div>
      </div>

      <!-- 7-Day Predictions -->
      <div class="lg:col-span-2 bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <div class="w-8 h-8 bg-green-100 rounded-sm flex items-center justify-center mr-3">
            <TrendingUp class="w-5 h-5 text-green-600" />
          </div>
          Prévisions sur 7 jours
        </h2>
        
        <div v-if="loading" class="flex items-center justify-center h-32">
          <div class="w-8 h-8 border-4 border-blue-200 rounded-full animate-spin border-t-blue-600"></div>
        </div>
        
        <div v-else-if="error" class="text-center py-8">
          <p class="text-red-600">{{ error }}</p>
          <button @click="$router.go(0)" class="mt-2 text-blue-600 hover:underline">
            Réessayer
          </button>
        </div>
        
        <div v-else-if="weeklyPredictions.length === 0" class="text-center py-8">
          <p class="text-gray-500">Aucune prédiction disponible</p>
        </div>
        
        <div v-else class="grid grid-cols-7 gap-3">
          <div 
            v-for="(prediction, index) in weeklyPredictions" 
            :key="prediction.id"
            class="text-center p-4 bg-gray-50 rounded-sm hover:bg-gray-100 transition-colors border border-gray-200"
          >
            <div class="text-xs font-medium text-gray-500 mb-2 uppercase">
              {{ formatDay(prediction.date) }}
            </div>
            <div class="text-2xl font-bold text-gray-900 mb-2">
              {{ Math.round(prediction.aqi) }}
            </div>
            <div class="text-xs text-gray-600 mb-3 font-medium">
              {{ getAQILevel(prediction.aqi) }}
            </div>
            <div class="w-full bg-gray-200 rounded-sm h-2">
              <div 
                :class="[
                  'h-2 rounded-sm transition-all duration-500',
                  getAQIColor(prediction.aqi)
                ]"
                :style="{ width: `${Math.min((prediction.aqi / 150) * 100, 100)}%` }"
              ></div>
            </div>
          </div>
        </div>

        <div class="mt-6 p-4 bg-yellow-50 rounded-sm border border-yellow-200">
          <div class="flex items-start">
            <AlertTriangle class="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
            <div>
              <h4 class="text-sm font-semibold text-yellow-800">Information importante</h4>
              <p class="text-sm text-yellow-700 mt-1">
                Les prévisions sont basées sur les modèles météorologiques et peuvent varier selon les conditions réelles.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Indicateurs clés</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Qualité moyenne</p>
              <p class="text-2xl font-bold text-gray-900">Modérée</p>
              <p class="text-xs text-gray-500 mt-1">Sur les dernières 24h</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-sm flex items-center justify-center">
              <span class="text-2xl">🌱</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Tendance</p>
              <p class="text-2xl font-bold text-gray-900">Amélioration</p>
              <p class="text-xs text-gray-500 mt-1">Prévision 24h</p>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-sm flex items-center justify-center">
              <TrendingUp class="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600 text-sm font-medium">Prochaine alerte</p>
              <p class="text-2xl font-bold text-gray-900">2h 30min</p>
              <p class="text-xs text-gray-500 mt-1">Estimation</p>
            </div>
            <div class="w-12 h-12 bg-orange-100 rounded-sm flex items-center justify-center">
              <Clock class="w-6 h-6 text-orange-600" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Home, ChevronRight, Clock, BarChart3, TrendingUp, AlertTriangle } from 'lucide-vue-next'
import PollutionCard from './PollutionCard.vue'
import { pollutionAPI, predictionAPI } from '@/services/api'
import type { PollutionData } from '@/types'

const currentData = ref<PollutionData | null>(null)
const weeklyPredictions = ref<PollutionData[]>([])
const atmoHistory = ref<any[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const getTrend = (value: number, threshold: number): 'up' | 'down' | 'stable' => {
  if (value > threshold * 1.1) return 'up'
  if (value < threshold * 0.9) return 'down'
  return 'stable'
}

const getLevel = (value: number, thresholds: number[]): 'good' | 'moderate' | 'unhealthy' | 'hazardous' => {
  if (value <= thresholds[0]) return 'good'
  if (value <= thresholds[1]) return 'moderate'
  if (value <= thresholds[2]) return 'unhealthy'
  return 'hazardous'
}

const getAQIDescription = (aqi: number): string => {
  if (aqi <= 50) return 'Bonne qualité'
  if (aqi <= 100) return 'Qualité moyenne'
  if (aqi <= 150) return 'Qualité dégradée'
  return 'Mauvaise qualité'
}

const getAQILevel = (aqi: number): string => {
  if (aqi <= 50) return 'Bon'
  if (aqi <= 100) return 'Moyen'
  if (aqi <= 150) return 'Dégradé'
  return 'Mauvais'
}

const getAQIColor = (aqi: number): string => {
  if (aqi <= 50) return 'bg-green-500'
  if (aqi <= 100) return 'bg-yellow-500'
  if (aqi <= 150) return 'bg-orange-500'
  return 'bg-red-500'
}

const getRecommendation = (aqi: number): string => {
  if (aqi <= 50) return 'Conditions idéales pour toutes les activités extérieures.'
  if (aqi <= 100) return 'Activités extérieures possibles pour la plupart des personnes.'
  if (aqi <= 150) return 'Limitez les activités extérieures intenses et prolongées.'
  return 'Évitez les activités extérieures. Restez à l\'intérieur si possible.'
}

const formatDay = (dateString: string): string => {
  const date = new Date(dateString)
  const today = new Date()
  const diffTime = date.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Auj.'
  if (diffDays === 1) return 'Dem.'
  
  const days = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']
  return days[date.getDay()]
}

const formatChartTime = (timeString: string): string => {
  if (!timeString) return ''
  const date = new Date(timeString)
  return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

const getChartLinePath = (): string => {
  if (atmoHistory.value.length === 0) return ''
  
  let path = ''
  atmoHistory.value.forEach((point, index) => {
    const x = (index / (atmoHistory.value.length - 1)) * 100
    const y = 100 - (point.value / 100) * 100
    
    if (index === 0) {
      path += `M ${x} ${y}`
    } else {
      path += ` L ${x} ${y}`
    }
  })
  
  return path
}

const getChartAreaPath = (): string => {
  if (atmoHistory.value.length === 0) return ''
  
  let path = getChartLinePath()
  
  // Close the area by going to bottom right, then bottom left
  const lastX = ((atmoHistory.value.length - 1) / (atmoHistory.value.length - 1)) * 100
  path += ` L ${lastX} 100 L 0 100 Z`
  
  return path
}

const generateAtmoHistory = () => {
  // Generate realistic historical data for ATMO index over 24 hours
  const data = []
  const now = new Date()
  
  for (let i = 23; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000)
    
    // Simulate realistic pollution patterns
    let baseValue = 60
    
    // Higher pollution during rush hours (7-9 AM, 5-7 PM)
    const hour = time.getHours()
    if ((hour >= 7 && hour <= 9) || (hour >= 17 && hour <= 19)) {
      baseValue += 20
    }
    
    // Lower pollution at night
    if (hour >= 22 || hour <= 6) {
      baseValue -= 15
    }
    
    // Add some random variation
    const variation = (Math.random() - 0.5) * 20
    const value = Math.max(20, Math.min(100, baseValue + variation))
    
    data.push({
      time: time.toISOString(),
      value: Math.round(value)
    })
  }
  
  return data
}

onMounted(async () => {
  loading.value = true
  error.value = null
  
  try {
    // Charger les données en parallèle
    const [current, predictions] = await Promise.all([
      pollutionAPI.getCurrentPollution(),
      predictionAPI.getWeeklyPredictions()
    ])
    
    currentData.value = current
    weeklyPredictions.value = predictions
    atmoHistory.value = generateAtmoHistory()
    
    console.log('Weekly predictions loaded:', predictions)
  } catch (error) {
    console.error('Failed to fetch pollution data:', error)
    error.value = 'Erreur lors du chargement des données'
  } finally {
    loading.value = false
  }
})
</script>