import type { User, PollutionData, AlertThreshold } from '@/types'

// Configuration de l'API
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Types pour les réponses API
interface ApiResponse<T> {
  data: T
  message?: string
  status: string
}

interface TokenResponse {
  access: string
  refresh: string
}

interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// Mock data for demonstration


const generateRealisticPollutionData = (): PollutionData => {
  const now = new Date()
  
  return {
    id: 'current',
    date: now.toISOString(),
    pm25: 42,
    pm10: 58,
    no2: 67,
    o3: 89,
    aqi: 84,
    location: 'Lyon, France',
    prediction: false
  }
}

const generateWeeklyPredictions = (): PollutionData[] => {
  const predictions: PollutionData[] = []
  const now = new Date()
  
  // Prédictions pour les 7 prochains jours
  for (let i = 1; i <= 7; i++) {
    const date = new Date(now)
    date.setDate(date.getDate() + i)
    
    // Simulation de variations réalistes selon le jour de la semaine
    const dayOfWeek = date.getDay()
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6
    
    let baseAQI = isWeekend ? 65 : 85
    
    // Tendance météo simulée (déterministe pour éviter les changements constants)
    const weatherFactor = 1 + Math.sin(i * 0.5) * 0.3
    const randomSeed = i * 123 // Seed déterministe basé sur le jour
    const pseudoRandom = (Math.sin(randomSeed) + 1) / 2 // Valeur entre 0 et 1
    const aqi = Math.max(30, baseAQI * weatherFactor + (pseudoRandom - 0.5) * 20)
    
    predictions.push({
      id: `week_${i}`,
      date: date.toISOString(),
      pm25: Math.round(aqi * 0.5),
      pm10: Math.round(aqi * 0.7),
      no2: Math.round(aqi * 0.8),
      o3: Math.round(aqi * 0.9),
      aqi: Math.round(aqi),
      location: 'Lyon, France',
      prediction: true
    })
  }
  
  return predictions
}

// Cache pour les prédictions hebdomadaires
let weeklyPredictionsCache: PollutionData[] | null = null
let cacheTimestamp: number = 0
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes
// Génération des alertes mockées
const generateMockAlerts = () => [
  {
    id: '1',
    type: 'warning',
    pollutant: 'PM2.5',
    value: 52,
    threshold: 50,
    location: 'Centre-ville Lyon',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    message: 'Dépassement du seuil PM2.5 détecté'
  },
  {
    id: '2',
    type: 'info',
    pollutant: 'O3',
    value: 95,
    threshold: 100,
    location: 'Part-Dieu',
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    message: 'Niveau O3 proche du seuil d\'alerte'
  },
  {
    id: '3',
    type: 'critical',
    pollutant: 'NO2',
    value: 125,
    threshold: 100,
    location: 'Périphérique Est',
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
    message: 'Alerte critique NO2 - Évitez les activités extérieures'
  }
]

// Gestion des tokens JWT
class TokenManager {
  private static ACCESS_TOKEN_KEY = 'access_token'
  private static REFRESH_TOKEN_KEY = 'refresh_token'

  static getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY)
  }

  static getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY)
  }

  static setTokens(access: string, refresh: string): void {
    localStorage.setItem(this.ACCESS_TOKEN_KEY, access)
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refresh)
  }

  static clearTokens(): void {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY)
    localStorage.removeItem(this.REFRESH_TOKEN_KEY)
  }
}

// Client HTTP avec gestion automatique des tokens
class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    console.log(this.baseURL + endpoint);
    const url = this.baseURL + endpoint
    const headers: Record<string, string> = options.headers ? { ...options.headers as any } : {}

    const accessToken = TokenManager.getAccessToken()
    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`
    }
    headers['Content-Type'] = 'application/json'

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      let errorData: any = {}
      try {
        errorData = await response.json()
      } catch {}
      throw new Error(errorData.message || response.statusText || 'Erreur API')
    }

    // Si pas de contenu (204), retourner null
    if (response.status === 204) return null as T
    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

const apiClient = new ApiClient(API_BASE_URL)

// Variable pour stocker l'utilisateur connecté
let currentUser: User | null = null

// Services API
export const authAPI = {
  
  async login(email: string, password: string): Promise<User> {
    const tokenResponse: TokenResponse = await apiClient.post('/users/login/', {
      email,
      password,
    })
    
    TokenManager.setTokens(tokenResponse.access, tokenResponse.refresh)
    
    // Récupérer les informations utilisateur
    const user: User = await apiClient.get('/users/me/')
    currentUser = user
    return user
  },

  async register(userData: {
    email: string
    password: string
    firstName: string
    lastName: string
    phone: string
  }): Promise<User> {
    const user: User = await apiClient.post('/users/register/', {
      email: userData.email,
      password: userData.password,
      first_name: userData.firstName,
      last_name: userData.lastName,
      phone: userData.phone,
    })
    
    // Connexion automatique après inscription
    await this.login(userData.email, userData.password)
    return user
  },

  async resetPassword(email: string): Promise<void> {
    await apiClient.post('/users/password-reset/', { email })
  },

  async confirmPasswordReset(token: string, password: string): Promise<void> {
    await apiClient.post('/users/password-reset/confirm/', {
      token,
      password,
    })
  },

  async getCurrentUser(): Promise<User | null> {
    try {
      if (currentUser) return currentUser
      const user: User = await apiClient.get('/users/me/')
      currentUser = user
      return user
    } catch (error) {
      return null
    }
  },

  async updateProfile(updates: Partial<User>): Promise<User> {
    const user: User = await apiClient.put('/users/me/', {
      threshold: updates.pollution_threshold,
      email: updates.email,
      phone: updates.phone,
      receive_alerts: updates.receive_alerts,
    })
    currentUser = user
    return user
  },

  async updateThreshold(thresholds: AlertThreshold): Promise<void> {
    await apiClient.put('/users/threshold/', {
      pm25: thresholds.pm25,
      pm10: thresholds.pm10,
      no2: thresholds.no2,
      o3: thresholds.o3,
    })
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await apiClient.post('/users/password-reset/', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  },

  async logout(): Promise<void> {
    TokenManager.clearTokens()
    currentUser = null
  },
}

export const pollutionAPI = {
  async getRawData(params?: {
    location?: string
    start_date?: string
    end_date?: string
    limit?: number
    offset?: number
  }): Promise<PaginatedResponse<any>> {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString())
        }
      })
    }
    
    const endpoint = `/data/raw/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
    return apiClient.get<PaginatedResponse<any>>(endpoint)
  },

  async getProcessedData(params?: {
    location?: string
    start_date?: string
    end_date?: string
    limit?: number
    offset?: number
  }): Promise<PaginatedResponse<PollutionData>> {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString())
        }
      })
    }
    
    const endpoint = `/data/processed/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
    return apiClient.get<PaginatedResponse<PollutionData>>(endpoint)
  },

  async getLatestData(location?: string): Promise<PollutionData> {
    const endpoint = `/data/latest/${location ? `?location=${location}` : ''}`
    return apiClient.get<PollutionData>(endpoint)
  },

  async getCurrentPollution(): Promise<PollutionData> {
    return this.getLatestData()
  },

  async getLocations(): Promise<string[]> {
    const response: { locations: string[] } = await apiClient.get('/data/locations/')
    return response.locations
  },

  async getStatistics(params?: {
    location?: string
    start_date?: string
    end_date?: string
  }): Promise<any> {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString())
        }
      })
    }
    
    const endpoint = `/data/statistics/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
    return apiClient.get(endpoint)
  },

  async getAlerts(): Promise<any[]> {
    // Cette route n'existe pas dans votre backend, on retourne les données mockées
    return generateMockAlerts()
  },
}

export const predictionAPI = {
  async getModels(): Promise<any[]> {
    const response: { models: any[] } = await apiClient.get('/predictions/models/')
    return response.models
  },

  async getActiveModel(): Promise<any> {
    return apiClient.get('/predictions/models/active/')
  },

  async getPredictions(params?: {
    location?: string
    start_date?: string
    end_date?: string
    limit?: number
    offset?: number
  }): Promise<PaginatedResponse<PollutionData>> {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString())
        }
      })
    }
    
    const endpoint = `/predictions/list/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
    return apiClient.get<PaginatedResponse<PollutionData>>(endpoint)
  },

  async getWeeklyPredictions(): Promise<PollutionData[]> {
    // Utiliser le cache si disponible et récent
    const now = Date.now()
    if (weeklyPredictionsCache && (now - cacheTimestamp) < CACHE_DURATION) {
      return weeklyPredictionsCache
    }
    
    // Générer de nouvelles prédictions
    weeklyPredictionsCache = generateWeeklyPredictions()
    cacheTimestamp = now
    
    // Simuler un délai réseau
    await new Promise(resolve => setTimeout(resolve, 300 + Math.random() * 400))
    
    return weeklyPredictionsCache
  },

  async getPredictionForLocation(location: string, date?: string): Promise<PollutionData> {
    return apiClient.post('/predictions/get/', {
      location,
      date: date || new Date().toISOString().split('T')[0],
    })
  },

  async getCustomPrediction(params: {
    location: string
    date: string
    weather_data?: any
    traffic_data?: any
  }): Promise<PollutionData> {
    return apiClient.post('/predictions/custom/', params)
  },

  async getTrainingHistory(): Promise<any[]> {
    const response: { history: any[] } = await apiClient.get('/predictions/training/history/')
    return response.history
  },

  async getEvaluationMetrics(): Promise<any> {
    return apiClient.get('/predictions/evaluation/')
  },
}

export const adminAPI = {
  async getUsers(params?: {
    role?: string
    email_alerts_enabled?: boolean
    limit?: number
    offset?: number
  }): Promise<User[]> {
    const queryParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString())
        }
      })
    }
    
    const endpoint = `/users/list/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
    const response: PaginatedResponse<User> = await apiClient.get(endpoint)
    return response.results
  },

  async getGlobalThresholds(): Promise<AlertThreshold> {
    // Cette route n'existe pas exactement, on retourne les seuils par défaut
    return {
      pm25: 35,
      pm10: 50,
      no2: 80,
      o3: 100,
    }
  },

  async updateGlobalThresholds(thresholds: AlertThreshold): Promise<void> {
    await apiClient.put('/users/threshold/default/', {
      pm25: thresholds.pm25,
      pm10: thresholds.pm10,
      no2: thresholds.no2,
      o3: thresholds.o3,
    })
  },

  async updateAtmoConfig(config: any): Promise<void> {
    // Cette route n'existe pas dans votre backend
    // Vous pourriez l'ajouter si nécessaire
    console.log('ATMO config update not implemented in backend:', config)
  },

  async clearData(): Promise<void> {
    await apiClient.post('/data/purge/')
  },

  async trainModel(): Promise<void> {
    await apiClient.post('/predictions/training/manual/')
  },

  async updateRemoteModel(): Promise<void> {
    await apiClient.post('/predictions/models/update-remote/')
  },

  async downloadRemoteModel(): Promise<void> {
    await apiClient.post('/predictions/models/download-remote/')
  },
}

// Export du client pour utilisation directe si nécessaire
export { apiClient }