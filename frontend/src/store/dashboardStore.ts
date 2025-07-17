import { create } from "zustand"
import axios from "axios"

interface DashboardMetrics {
  total_revenue: number
  total_orders: number
  avg_order_value: number
  total_ad_spend: number
  roas: number
  conversion_rate: number
  total_sessions: number
  bounce_rate: number
}

interface PlatformMetrics {
  platform: string
  revenue: number
  orders: number
  sessions: number
  conversion_rate: number
}

interface DashboardStore {
  metrics: DashboardMetrics | null
  platformMetrics: PlatformMetrics[]
  chartData: any[]
  timeRange: string
  selectedPlatforms: string[]
  isLoading: boolean
  fetchMetrics: () => Promise<void>
  fetchPlatformMetrics: () => Promise<void>
  fetchChartData: (chartType: string) => Promise<void>
  setTimeRange: (range: string) => void
  setSelectedPlatforms: (platforms: string[]) => void
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export const useDashboardStore = create<DashboardStore>((set, get) => ({
  metrics: null,
  platformMetrics: [],
  chartData: [],
  timeRange: "30d",
  selectedPlatforms: ["all"],
  isLoading: false,

  fetchMetrics: async () => {
    set({ isLoading: true })
    try {
      const { timeRange, selectedPlatforms } = get()
      const platformsQuery = selectedPlatforms.includes("all") ? "all" : selectedPlatforms.join(",")

      const response = await axios.get(`${API_BASE_URL}/api/dashboard/metrics`, {
        params: { time_range: timeRange, platforms: platformsQuery },
      })

      set({ metrics: response.data, isLoading: false })
    } catch (error) {
      console.error("Failed to fetch metrics:", error)
      set({ isLoading: false })
    }
  },

  fetchPlatformMetrics: async () => {
    try {
      const { timeRange } = get()
      const response = await axios.get(`${API_BASE_URL}/api/dashboard/platform-metrics`, {
        params: { time_range: timeRange },
      })

      set({ platformMetrics: response.data })
    } catch (error) {
      console.error("Failed to fetch platform metrics:", error)
    }
  },

  fetchChartData: async (chartType: string) => {
    try {
      const { timeRange } = get()
      const response = await axios.get(`${API_BASE_URL}/api/dashboard/chart-data`, {
        params: { chart_type: chartType, time_range: timeRange },
      })

      set({ chartData: response.data })
    } catch (error) {
      console.error("Failed to fetch chart data:", error)
    }
  },

  setTimeRange: (range: string) => {
    set({ timeRange: range })
    get().fetchMetrics()
  },

  setSelectedPlatforms: (platforms: string[]) => {
    set({ selectedPlatforms: platforms })
    get().fetchMetrics()
  },
}))
