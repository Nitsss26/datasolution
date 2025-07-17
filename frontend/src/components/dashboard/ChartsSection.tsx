"use client"

import { useEffect } from "react"
import { useDashboardStore } from "@/store/dashboardStore"
import { motion } from "framer-motion"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  AreaChart,
  Area,
} from "recharts"

const COLORS = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#F97316"]

export default function ChartsSection() {
  const { chartData, fetchChartData } = useDashboardStore()

  useEffect(() => {
    fetchChartData("revenue_trend")
  }, [fetchChartData])

  // Mock data for demonstration
  const revenueData = [
    { date: "2024-01-01", revenue: 12500, orders: 45 },
    { date: "2024-01-02", revenue: 15800, orders: 52 },
    { date: "2024-01-03", revenue: 14200, orders: 48 },
    { date: "2024-01-04", revenue: 18600, orders: 61 },
    { date: "2024-01-05", revenue: 16400, orders: 55 },
    { date: "2024-01-06", revenue: 19200, orders: 67 },
    { date: "2024-01-07", revenue: 22100, orders: 73 },
  ]

  const platformData = [
    { platform: "Shopify", revenue: 45000, color: "#10B981" },
    { platform: "Facebook Ads", revenue: 28000, color: "#3B82F6" },
    { platform: "Google Ads", revenue: 32000, color: "#F59E0B" },
    { platform: "Shiprocket", revenue: 15000, color: "#EF4444" },
  ]

  const conversionFunnelData = [
    { stage: "Impressions", value: 150000, color: "#3B82F6" },
    { stage: "Clicks", value: 12000, color: "#10B981" },
    { stage: "Sessions", value: 8500, color: "#F59E0B" },
    { stage: "Orders", value: 450, color: "#EF4444" },
  ]

  const adPerformanceData = [
    { campaign: "Holiday Sale", spend: 5000, revenue: 22000, roas: 4.4 },
    { campaign: "New Product Launch", spend: 3500, revenue: 14000, roas: 4.0 },
    { campaign: "Retargeting", spend: 2000, revenue: 9000, roas: 4.5 },
    { campaign: "Brand Awareness", spend: 4000, revenue: 12000, roas: 3.0 },
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Revenue Trend */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-sm p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue Trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={revenueData}>
            <defs>
              <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip
              formatter={(value, name) => [`$${value.toLocaleString()}`, "Revenue"]}
              labelFormatter={(label) => `Date: ${label}`}
            />
            <Area type="monotone" dataKey="revenue" stroke="#3B82F6" fillOpacity={1} fill="url(#colorRevenue)" />
          </AreaChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Platform Revenue */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl shadow-sm p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue by Platform</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={platformData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="platform" />
            <YAxis />
            <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, "Revenue"]} />
            <Bar dataKey="revenue" fill="#3B82F6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Conversion Funnel */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-xl shadow-sm p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Conversion Funnel</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={conversionFunnelData} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="stage" type="category" />
            <Tooltip formatter={(value) => [value.toLocaleString(), "Count"]} />
            <Bar dataKey="value" fill="#10B981" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Ad Performance */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-xl shadow-sm p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Ad Campaign Performance</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={adPerformanceData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="campaign" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="roas" stroke="#3B82F6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>
    </div>
  )
}
