"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuthStore } from "@/store/authStore"
import DashboardLayout from "@/components/layout/DashboardLayout"
import MetricsCards from "@/components/dashboard/MetricsCards"
import ChartsSection from "@/components/dashboard/ChartsSection"
import PlatformMetrics from "@/components/dashboard/PlatformMetrics"
import { useDashboardStore } from "@/store/dashboardStore"

export default function Dashboard() {
  const { user } = useAuthStore()
  const { timeRange, selectedPlatforms, fetchMetrics } = useDashboardStore()
  const router = useRouter()

  useEffect(() => {
    if (!user) {
      router.push("/")
      return
    }

    fetchMetrics()
  }, [user, router, timeRange, selectedPlatforms, fetchMetrics])

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <div className="text-sm text-gray-500">Welcome back, {user.full_name}</div>
        </div>

        <MetricsCards />
        <ChartsSection />
        <PlatformMetrics />
      </div>
    </DashboardLayout>
  )
}
