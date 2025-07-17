"use client"

import type React from "react"

import { useState } from "react"
import { useAuthStore } from "@/store/authStore"
import { useDashboardStore } from "@/store/dashboardStore"
import { BarChart3, Settings, LogOut, Menu, X, Home, TrendingUp, Users } from "lucide-react"

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user, logout } = useAuthStore()
  const { timeRange, setTimeRange, selectedPlatforms, setSelectedPlatforms } = useDashboardStore()

  const navigation = [
    { name: "Dashboard", href: "/dashboard", icon: Home, current: true },
    { name: "Analytics", href: "/analytics", icon: TrendingUp, current: false },
    { name: "Integrations", href: "/integrations", icon: Settings, current: false },
    { name: "Reports", href: "/reports", icon: BarChart3, current: false },
  ]

  const platforms = [
    { id: "shopify", name: "Shopify", color: "bg-green-500" },
    { id: "facebook_ads", name: "Facebook Ads", color: "bg-blue-500" },
    { id: "google_ads", name: "Google Ads", color: "bg-red-500" },
    { id: "shiprocket", name: "Shiprocket", color: "bg-purple-500" },
  ]

  const timeRanges = [
    { id: "7d", name: "7 Days" },
    { id: "15d", name: "15 Days" },
    { id: "30d", name: "30 Days" },
    { id: "90d", name: "90 Days" },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} lg:translate-x-0 transition-transform duration-200 ease-in-out`}
      >
        <div className="flex items-center justify-between h-16 px-4 border-b">
          <h2 className="text-xl font-semibold text-gray-900">D2C Analytics</h2>
          <button onClick={() => setSidebarOpen(false)} className="lg:hidden">
            <X size={24} />
          </button>
        </div>

        <nav className="mt-8">
          <div className="px-4 space-y-2">
            {navigation.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className={`flex items-center px-3 py-2 rounded-lg text-sm font-medium ${
                  item.current ? "bg-blue-50 text-blue-700" : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                }`}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </a>
            ))}
          </div>
        </nav>

        <div className="mt-8 px-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Filters</h3>

          {/* Time Range Filter */}
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Time Range</label>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {timeRanges.map((range) => (
                <option key={range.id} value={range.id}>
                  {range.name}
                </option>
              ))}
            </select>
          </div>

          {/* Platform Filter */}
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Platforms</label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedPlatforms.includes("all")}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedPlatforms(["all"])
                    } else {
                      setSelectedPlatforms([])
                    }
                  }}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700">All Platforms</span>
              </label>

              {platforms.map((platform) => (
                <label key={platform.id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedPlatforms.includes(platform.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedPlatforms([...selectedPlatforms.filter((p) => p !== "all"), platform.id])
                      } else {
                        setSelectedPlatforms(selectedPlatforms.filter((p) => p !== platform.id))
                      }
                    }}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <div className={`ml-2 w-3 h-3 rounded-full ${platform.color}`}></div>
                  <span className="ml-2 text-sm text-gray-700">{platform.name}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              <Users size={16} />
            </div>
            <div>
              <div className="text-sm font-medium text-gray-900">{user?.full_name}</div>
              <div className="text-xs text-gray-500">{user?.company_name}</div>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center w-full px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg"
          >
            <LogOut className="mr-3 h-4 w-4" />
            Logout
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:ml-64">
        {/* Top header */}
        <div className="bg-white shadow-sm border-b">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <button onClick={() => setSidebarOpen(true)} className="lg:hidden">
                <Menu size={24} />
              </button>

              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-500">Last updated: {new Date().toLocaleString()}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-4 sm:p-6 lg:p-8">{children}</main>
      </div>

      {/* Sidebar backdrop */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}
    </div>
  )
}
