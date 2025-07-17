"use client"

import { useDashboardStore } from "@/store/dashboardStore"
import { motion } from "framer-motion"
import { DollarSign, ShoppingCart, TrendingUp, Users, Target, MousePointer, Eye, BarChart3 } from "lucide-react"

export default function MetricsCards() {
  const { metrics, isLoading } = useDashboardStore()

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <div key={i} className="bg-white rounded-xl shadow-sm p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    )
  }

  if (!metrics) return null

  const cards = [
    {
      title: "Total Revenue",
      value: `$${metrics.total_revenue.toLocaleString()}`,
      icon: DollarSign,
      color: "bg-green-500",
      change: "+12.5%",
      changeType: "positive",
    },
    {
      title: "Total Orders",
      value: metrics.total_orders.toLocaleString(),
      icon: ShoppingCart,
      color: "bg-blue-500",
      change: "+8.2%",
      changeType: "positive",
    },
    {
      title: "Average Order Value",
      value: `$${metrics.avg_order_value.toFixed(2)}`,
      icon: TrendingUp,
      color: "bg-purple-500",
      change: "+3.1%",
      changeType: "positive",
    },
    {
      title: "Ad Spend",
      value: `$${metrics.total_ad_spend.toLocaleString()}`,
      icon: Target,
      color: "bg-red-500",
      change: "+15.3%",
      changeType: "negative",
    },
    {
      title: "ROAS",
      value: `${metrics.roas.toFixed(2)}x`,
      icon: BarChart3,
      color: "bg-yellow-500",
      change: "+0.3x",
      changeType: "positive",
    },
    {
      title: "Conversion Rate",
      value: `${metrics.conversion_rate.toFixed(1)}%`,
      icon: MousePointer,
      color: "bg-indigo-500",
      change: "+1.2%",
      changeType: "positive",
    },
    {
      title: "Sessions",
      value: metrics.total_sessions.toLocaleString(),
      icon: Users,
      color: "bg-pink-500",
      change: "+18.7%",
      changeType: "positive",
    },
    {
      title: "Bounce Rate",
      value: `${metrics.bounce_rate.toFixed(1)}%`,
      icon: Eye,
      color: "bg-orange-500",
      change: "-2.1%",
      changeType: "positive",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <motion.div
          key={card.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow"
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`p-3 rounded-lg ${card.color}`}>
              <card.icon className="h-6 w-6 text-white" />
            </div>
            <div
              className={`text-sm font-medium ${card.changeType === "positive" ? "text-green-600" : "text-red-600"}`}
            >
              {card.change}
            </div>
          </div>
          <div className="mb-1">
            <div className="text-2xl font-bold text-gray-900">{card.value}</div>
          </div>
          <div className="text-sm text-gray-500">{card.title}</div>
        </motion.div>
      ))}
    </div>
  )
}
