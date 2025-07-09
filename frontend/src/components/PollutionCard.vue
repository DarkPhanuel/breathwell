<template>
  <div class="bg-white rounded-sm shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="text-2xl">{{ icon }}</div>
        <div>
          <h3 class="text-gray-900 font-semibold text-lg">{{ title }}</h3>
          <p class="text-gray-500 text-xs">{{ description }}</p>
        </div>
      </div>
    </div>
    
    <!-- Value Display -->
    <div class="mb-6">
      <div class="flex items-end space-x-2 mb-2">
        <span class="text-3xl font-bold text-gray-900">{{ value }}</span>
        <span class="text-sm text-gray-500 mb-1">{{ unit }}</span>
      </div>
      
      <!-- Trend and Level -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <component 
            :is="TrendIcon" 
            :class="[
              'w-4 h-4',
              trend === 'up' ? 'text-red-500' : 
              trend === 'down' ? 'text-green-500' : 
              'text-gray-400'
            ]" 
          />
          <span class="text-sm text-gray-600">{{ trendText }}</span>
        </div>
        
        <div :class="[
          'px-2 py-1 rounded-full text-xs font-medium',
          levelStyles[level]
        ]">
          {{ levelText }}
        </div>
      </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="space-y-2">
      <div class="w-full bg-gray-200 rounded-sm h-2">
        <div 
          :class="[
            'h-2 rounded-sm transition-all duration-1000',
            levelColors[level]
          ]"
          :style="{ width: `${Math.min((value / maxValue) * 100, 100)}%` }"
        ></div>
      </div>
      
      <!-- Threshold indicators -->
      <div class="flex justify-between text-xs text-gray-400">
        <span>0</span>
        <span>{{ Math.round(maxValue / 2) }}</span>
        <span>{{ maxValue }}</span>
      </div>
    </div>

    <!-- Health Impact -->
    <div class="mt-4 p-3 bg-gray-50 rounded-sm">
      <p class="text-xs text-gray-600">
        <span class="font-medium text-gray-700">Impact santé:</span>
        {{ getHealthImpact(level) }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TrendingUp, TrendingDown, Minus } from 'lucide-vue-next'

interface Props {
  title: string
  value: number
  unit: string
  trend: 'up' | 'down' | 'stable'
  level: 'good' | 'moderate' | 'unhealthy' | 'hazardous'
  maxValue?: number
  icon?: string
  description?: string
}

const props = withDefaults(defineProps<Props>(), {
  maxValue: 200,
  icon: '🌫️',
  description: 'Polluant atmosphérique'
})

const levelColors = {
  good: 'bg-green-500',
  moderate: 'bg-yellow-500',
  unhealthy: 'bg-orange-500',
  hazardous: 'bg-red-500'
}

const levelStyles = {
  good: 'bg-green-100 text-green-800',
  moderate: 'bg-yellow-100 text-yellow-800',
  unhealthy: 'bg-orange-100 text-orange-800',
  hazardous: 'bg-red-100 text-red-800'
}

const trendText = computed(() => {
  switch (props.trend) {
    case 'up': return 'En hausse'
    case 'down': return 'En baisse'
    default: return 'Stable'
  }
})

const levelText = computed(() => {
  switch (props.level) {
    case 'good': return 'Bon'
    case 'moderate': return 'Modéré'
    case 'unhealthy': return 'Mauvais'
    case 'hazardous': return 'Dangereux'
    default: return props.level
  }
})

const getHealthImpact = (level: string): string => {
  switch (level) {
    case 'good': return 'Aucun impact sur la santé'
    case 'moderate': return 'Impact limité pour les personnes sensibles'
    case 'unhealthy': return 'Peut affecter les personnes sensibles'
    case 'hazardous': return 'Dangereux pour tous'
    default: return 'Impact inconnu'
  }
}

const TrendIcon = computed(() => {
  switch (props.trend) {
    case 'up': return TrendingUp
    case 'down': return TrendingDown
    default: return Minus
  }
})
</script>