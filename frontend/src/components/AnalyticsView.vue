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
            <span class="ml-2 text-sm font-medium text-gray-900">Analyses avancées</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Header -->
    <div class="border-b border-gray-200 pb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Analyses avancées</h1>
      <p class="text-gray-600">
        Insights et tendances de la qualité de l'air basés sur l'intelligence artificielle.
      </p>
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-blue-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">📊</span>
          </div>
          <div class="text-right">
            <p class="text-gray-600 text-sm font-medium">Précision IA</p>
            <p class="text-3xl font-bold text-gray-900">94.2%</p>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-sm h-2">
          <div class="bg-blue-600 h-2 rounded-sm" style="width: 94.2%"></div>
        </div>
      </div>

      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-green-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">📈</span>
          </div>
          <div class="text-right">
            <p class="text-gray-600 text-sm font-medium">Amélioration</p>
            <p class="text-3xl font-bold text-gray-900">+12%</p>
          </div>
        </div>
        <p class="text-gray-600 text-sm">vs mois dernier</p>
      </div>

      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-red-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">🎯</span>
          </div>
          <div class="text-right">
            <p class="text-gray-600 text-sm font-medium">Alertes évitées</p>
            <p class="text-3xl font-bold text-gray-900">847</p>
          </div>
        </div>
        <p class="text-gray-600 text-sm">grâce aux prédictions</p>
      </div>

      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="w-12 h-12 bg-gray-100 rounded-sm flex items-center justify-center">
            <span class="text-2xl">⚡</span>
          </div>
          <div class="text-right">
            <p class="text-gray-600 text-sm font-medium">Temps réponse</p>
            <p class="text-3xl font-bold text-gray-900">1.2s</p>
          </div>
        </div>
        <p class="text-gray-600 text-sm">temps moyen</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Trend Chart -->
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <span class="w-8 h-8 bg-blue-100 rounded-sm flex items-center justify-center mr-3 text-sm">
            📈
          </span>
          Tendances mensuelles
        </h2>
        
        <div class="h-64 bg-gray-50 rounded-sm flex items-center justify-center border border-gray-200">
          <div class="text-center">
            <div class="w-16 h-16 bg-blue-600 rounded-sm flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl text-white">📊</span>
            </div>
            <p class="text-gray-700 text-lg font-medium">Graphique des tendances</p>
            <p class="text-gray-500 text-sm mt-2">Évolution des polluants sur 12 mois</p>
          </div>
        </div>
      </div>

      <!-- Distribution Chart -->
      <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <span class="w-8 h-8 bg-green-100 rounded-sm flex items-center justify-center mr-3 text-sm">
            🥧
          </span>
          Répartition AQI
        </h2>
        
        <div class="h-64 bg-gray-50 rounded-sm flex items-center justify-center border border-gray-200">
          <div class="text-center">
            <div class="w-16 h-16 bg-green-600 rounded-sm flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl text-white">🥧</span>
            </div>
            <p class="text-gray-700 text-lg font-medium">Graphique en secteurs</p>
            <p class="text-gray-500 text-sm mt-2">Distribution des niveaux de qualité</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Analytics -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
        <span class="w-8 h-8 bg-red-100 rounded-sm flex items-center justify-center mr-3 text-sm">
          🔍
        </span>
        Analyse détaillée par polluant
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="pollutant in pollutantStats" :key="pollutant.name" 
             class="bg-gray-50 rounded-sm p-4 border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-gray-900 font-bold">{{ pollutant.name }}</h3>
            <span class="text-2xl">{{ pollutant.icon }}</span>
          </div>
          
          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Moyenne</span>
              <span class="text-gray-900 font-medium">{{ pollutant.average }} μg/m³</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Maximum</span>
              <span class="text-gray-900 font-medium">{{ pollutant.max }} μg/m³</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Tendance</span>
              <span :class="[
                'font-medium',
                pollutant.trend === 'up' ? 'text-red-600' : 
                pollutant.trend === 'down' ? 'text-green-600' : 'text-gray-600'
              ]">
                {{ getTrendText(pollutant.trend) }}
              </span>
            </div>
            
            <div class="w-full bg-gray-300 rounded-sm h-2 mt-3">
              <div 
                :class="[
                  'h-2 rounded-sm transition-all duration-1000',
                  getPollutantColor(pollutant.level)
                ]"
                :style="{ width: `${(pollutant.average / pollutant.threshold) * 100}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Predictions Accuracy -->
    <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 flex items-center">
        <span class="w-8 h-8 bg-blue-100 rounded-sm flex items-center justify-center mr-3 text-sm">
          🎯
        </span>
        Précision des prédictions
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="text-center bg-gray-50 rounded-sm p-6 border border-gray-200">
          <div class="text-4xl font-bold text-gray-900 mb-2">96.8%</div>
          <p class="text-gray-600 text-sm">Prédictions 1h</p>
          <div class="w-full bg-gray-300 rounded-sm h-2 mt-2">
            <div class="bg-green-600 h-2 rounded-sm" style="width: 96.8%"></div>
          </div>
        </div>
        
        <div class="text-center bg-gray-50 rounded-sm p-6 border border-gray-200">
          <div class="text-4xl font-bold text-gray-900 mb-2">94.2%</div>
          <p class="text-gray-600 text-sm">Prédictions 6h</p>
          <div class="w-full bg-gray-300 rounded-sm h-2 mt-2">
            <div class="bg-blue-600 h-2 rounded-sm" style="width: 94.2%"></div>
          </div>
        </div>
        
        <div class="text-center bg-gray-50 rounded-sm p-6 border border-gray-200">
          <div class="text-4xl font-bold text-gray-900 mb-2">89.5%</div>
          <p class="text-gray-600 text-sm">Prédictions 24h</p>
          <div class="w-full bg-gray-300 rounded-sm h-2 mt-2">
            <div class="bg-red-600 h-2 rounded-sm" style="width: 89.5%"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Information Panel -->
    <div class="bg-blue-50 rounded-sm border border-blue-200 p-6">
      <div class="flex items-start">
        <Info class="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
        <div>
          <h3 class="text-blue-900 font-semibold mb-2">Méthodologie d'analyse</h3>
          <p class="text-blue-800 text-sm leading-relaxed">
            Les analyses sont basées sur des algorithmes d'apprentissage automatique entraînés sur les données historiques 
            de qualité de l'air. Les prédictions utilisent des modèles météorologiques et des données de trafic en temps réel 
            pour optimiser la précision des forecasts.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Home, ChevronRight, Info } from 'lucide-vue-next'
import { predictionAPI } from '@/services/api'

const pollutantStats = ref([
  {
    name: 'PM2.5',
    icon: '🌫️',
    average: 32,
    max: 78,
    trend: 'down',
    level: 'moderate',
    threshold: 50
  },
  {
    name: 'PM10',
    icon: '💨',
    average: 45,
    max: 92,
    trend: 'stable',
    level: 'moderate',
    threshold: 80
  },
  {
    name: 'NO2',
    icon: '🚗',
    average: 58,
    max: 125,
    trend: 'up',
    level: 'unhealthy',
    threshold: 100
  },
  {
    name: 'O3',
    icon: '☀️',
    average: 67,
    max: 134,
    trend: 'down',
    level: 'moderate',
    threshold: 120
  }
])

const getTrendText = (trend: string): string => {
  switch (trend) {
    case 'up': return '↗️ Hausse'
    case 'down': return '↘️ Baisse'
    default: return '➡️ Stable'
  }
}

const getPollutantColor = (level: string): string => {
  switch (level) {
    case 'good': return 'bg-green-600'
    case 'moderate': return 'bg-yellow-600'
    case 'unhealthy': return 'bg-red-600'
    case 'hazardous': return 'bg-red-800'
    default: return 'bg-gray-600'
  }
}
</script>