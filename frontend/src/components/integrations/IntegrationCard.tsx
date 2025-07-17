"use client"

import { motion } from "framer-motion"
import { Check, Plus, RefreshCw } from "lucide-react"

interface IntegrationCardProps {
  integration: {
    id: string
    name: string
    description: string
    icon: string
    color: string
  }
  isConnected: boolean
  lastSync: string | null
  onConnect: () => void
  onSync: () => void
  isSyncing: boolean
}

export default function IntegrationCard({
  integration,
  isConnected,
  lastSync,
  onConnect,
  onSync,
  isSyncing,
}: IntegrationCardProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Never"
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-3 rounded-lg ${integration.color}`}>
            <span className="text-2xl">{integration.icon}</span>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{integration.name}</h3>
            <div className="flex items-center space-x-2 mt-1">
              {isConnected ? (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  <Check size={12} className="mr-1" />
                  Connected
                </span>
              ) : (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  Not Connected
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      <p className="text-sm text-gray-600 mb-4">{integration.description}</p>

      {isConnected && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Last Sync:</span>
            <span className="text-gray-900 font-medium">{formatDate(lastSync)}</span>
          </div>
        </div>
      )}

      <div className="flex space-x-3">
        {!isConnected ? (
          <button
            onClick={onConnect}
            className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus size={16} />
            <span>Connect</span>
          </button>
        ) : (
          <button
            onClick={onSync}
            disabled={isSyncing}
            className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <RefreshCw size={16} className={isSyncing ? "animate-spin" : ""} />
            <span>{isSyncing ? "Syncing..." : "Sync Data"}</span>
          </button>
        )}
      </div>
    </motion.div>
  )
}
