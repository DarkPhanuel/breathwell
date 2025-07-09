export interface User {
  id: string
  email: string
  phone: string
  is_admin: boolean
  pollution_threshold: number
  receive_alerts: boolean
  "date_joined": "2025-07-08T16:08:41.245405Z"
}

export interface PollutionData {
  id: string
  date: string
  pm25: number
  pm10: number
  no2: number
  o3: number
  aqi: number
  location: string
  prediction: boolean
}

export interface AlertThreshold {
  pm25: number
  pm10: number
  no2: number
  o3: number
  atmo?: number
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
}

export interface PollutionLevel {
  level: 'good' | 'moderate' | 'unhealthy' | 'hazardous'
  color: string
  description: string
}

export interface ApiError {
  message: string
  status: number
  details?: any
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}