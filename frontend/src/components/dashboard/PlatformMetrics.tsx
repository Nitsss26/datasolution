"use client"

import { useEffect } from "react"
import { useDashboardStore } from "@/store/dashboardStore"
import { motion } from "framer-motion"
import { TrendingUp } from "lucide-react"

export default function PlatformMetrics() {
  const { platformMetrics, fetchPlatformMetrics } = useDashboardStore()

  useEffect(() => {
    fetchPlatformMetrics()
  }, [fetchPlatformMetrics])

  const platformIcons = {
    shopify: "🛍️",
    facebook_ads: "📘",
    google_ads: "🔍",
    shiprocket: "📦",
  }

  const platformColors = {
    shopify: "bg-green-50 border-green-200",
    facebook_ads: "bg-blue-50 border-blue-200",
    google_ads: "bg-red-50 border-red-200",
    shiprocket: "bg-purple-50 border-purple-200",
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
      className="bg-white rounded-xl shadow-sm p-6"
    >
      <h3 className="text-lg font-semibold text-gray-900 mb-6">Platform Performance</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {platformMetrics.map((platform, index) => (
          <div
            key={platform.platform}
            className={`p-4 rounded-lg border-2 ${platformColors[platform.platform as keyof typeof platformColors] || "bg-gray-50 border-gray-200"}`}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <span className="text-2xl">
                  {platformIcons[platform.platform as keyof typeof platformIcons] || "📊"}
                </span>
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {platform.platform.replace("_", " ")}
                </span>
              </div>
              <div className="flex items-center text-green-600">
                <TrendingUp size={16} />
                <span className="text-xs ml-1">+12%</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-xs text-gray-500">Revenue</span>
                <span className="text-sm font-semibold">${platform.revenue.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-xs text-gray-500">Orders</span>
                <span className="text-sm font-semibold">{platform.orders}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-xs text-gray-500">Sessions</span>
                <span className="text-sm font-semibold">{platform.sessions.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-xs text-gray-500">Conv. Rate</span>
                <span className="text-sm font-semibold">{platform.conversion_rate.toFixed(1)}%</span>
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-gray-200">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(platform.conversion_rate * 10, 100)}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}
