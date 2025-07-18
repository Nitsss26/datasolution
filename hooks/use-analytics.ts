'use client'

import { useState, useEffect } from 'react'
import type { DashboardData } from '@/types/analytics'

interface UseAnalyticsProps {
  platforms: string[]
  timeRange: string
  demoMode?: boolean
}

interface UseAnalyticsReturn {
  data: DashboardData | null
  isLoading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export function useAnalytics({ platforms, timeRange, demoMode = false }: UseAnalyticsProps): UseAnalyticsReturn {
  const [data, setData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchAnalytics = async () => {
    try {
      setIsLoading(true)
      setError(null)

      let endpoint = demoMode 
        ? '/api/demo/analytics'
        : `${process.env.NEXT_PUBLIC_API_URL}/analytics`

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          platforms,
          timeRange,
          demoMode,
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const analyticsData = await response.json()
      setData(analyticsData)
    } catch (err) {
      console.error('Analytics fetch error:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics data')
    } finally {
      setIsLoading(false)
    }
  }

  const refetch = async () => {
    await fetchAnalytics()
  }

  useEffect(() => {
    fetchAnalytics()
  }, [platforms, timeRange, demoMode])

  return {
    data,
    isLoading,
    error,
    refetch,
  }
}