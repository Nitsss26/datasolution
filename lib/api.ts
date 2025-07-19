import axios from 'axios'
import toast from 'react-hot-toast'

// API Configuration for your VM
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'http://82.29.164.244:8000' 
  : 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    toast.error(message)
    
    return Promise.reject(error)
  }
)

// API Functions
export const apiService = {
  // Analytics
  getAnalytics: (params?: any) => api.get('/api/analytics', { params }),
  getDemoAnalytics: () => api.get('/api/demo/analytics'),
  
  // Platform Management
  getPlatformStatus: () => api.get('/api/platforms/status'),
  connectPlatform: (platform: string, credentials: any) => 
    api.post(`/api/integrations/${platform}/connect`, credentials),
  disconnectPlatform: (platform: string) => 
    api.post(`/api/integrations/${platform}/disconnect`),
  syncPlatform: (platform: string) => 
    api.post(`/api/pipeline/sync-platform/${platform}`),
  
  // BigQuery Management
  getBigQueryStatus: () => api.get('/api/bigquery/status'),
  setupBigQuery: (config: any) => api.post('/api/bigquery/setup', config),
  testBigQueryConnection: (config: any) => api.post('/api/bigquery/test', config),
  
  // Pipeline Management
  getPipelineStatus: () => api.get('/api/pipeline/status'),
  startPipeline: () => api.post('/api/pipeline/start'),
  stopPipeline: () => api.post('/api/pipeline/stop'),
  getPipelineLogs: () => api.get('/api/pipeline/logs'),
  
  // P&L Reports
  getPLReport: (params?: any) => api.get('/api/analytics/pl-report', { params }),
  exportPLReport: (params?: any) => api.get('/api/export/pl', { params, responseType: 'blob' }),
  
  // AI Insights
  getAIInsights: (query: string) => api.post('/api/ai/query', { query }),
  
  // User Preferences
  getUserPreferences: () => api.get('/api/user/preferences'),
  saveUserPreferences: (preferences: any) => api.post('/api/user/preferences', preferences),
}

export default api