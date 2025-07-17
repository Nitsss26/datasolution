"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuthStore } from "@/store/authStore"
import DashboardLayout from "@/components/layout/DashboardLayout"
import IntegrationCard from "@/components/integrations/IntegrationCard"
import IntegrationModal from "@/components/integrations/IntegrationModal"
import { motion } from "framer-motion"
import { RefreshCw } from "lucide-react"
import axios from "axios"
import { toast } from "react-hot-toast"

interface Integration {
  platform: string
  is_active: boolean
  created_at: string
  last_sync: string | null
}

export default function IntegrationsPage() {
  const [integrations, setIntegrations] = useState<Integration[]>([])
  const [selectedIntegration, setSelectedIntegration] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isSyncing, setIsSyncing] = useState<string | null>(null)

  const { user } = useAuthStore()
  const router = useRouter()

  const availableIntegrations = [
    {
      id: "shopify",
      name: "Shopify",
      description: "Connect your Shopify store to sync sales, orders, and inventory data",
      icon: "🛍️",
      color: "bg-green-500",
      fields: [
        { name: "shop_url", label: "Shop URL", type: "text", placeholder: "your-shop-name" },
        { name: "access_token", label: "Access Token", type: "password", placeholder: "Your Shopify access token" },
      ],
    },
    {
      id: "facebook_ads",
      name: "Facebook Ads",
      description: "Sync your Facebook ad campaigns, spend, and performance metrics",
      icon: "📘",
      color: "bg-blue-500",
      fields: [
        { name: "access_token", label: "Access Token", type: "password", placeholder: "Your Facebook access token" },
        { name: "ad_account_id", label: "Ad Account ID", type: "text", placeholder: "act_123456789" },
      ],
    },
    {
      id: "google_ads",
      name: "Google Ads",
      description: "Import Google Ads data including campaigns, keywords, and conversions",
      icon: "🔍",
      color: "bg-red-500",
      fields: [
        { name: "access_token", label: "Access Token", type: "password", placeholder: "Your Google Ads access token" },
        { name: "customer_id", label: "Customer ID", type: "text", placeholder: "123-456-7890" },
        { name: "developer_token", label: "Developer Token", type: "password", placeholder: "Your developer token" },
      ],
    },
    {
      id: "shiprocket",
      name: "Shiprocket",
      description: "Track shipping costs, delivery times, and logistics data",
      icon: "📦",
      color: "bg-purple-500",
      fields: [
        { name: "email", label: "Email", type: "email", placeholder: "your-email@example.com" },
        { name: "password", label: "Password", type: "password", placeholder: "Your Shiprocket password" },
      ],
    },
  ]

  useEffect(() => {
    if (!user) {
      router.push("/")
      return
    }

    fetchIntegrations()
  }, [user, router])

  const fetchIntegrations = async () => {
    setIsLoading(true)
    try {
      const response = await axios.get("/api/integrations/")
      setIntegrations(response.data)
    } catch (error) {
      toast.error("Failed to fetch integrations")
    } finally {
      setIsLoading(false)
    }
  }

  const handleConnect = (platformId: string) => {
    setSelectedIntegration(platformId)
    setIsModalOpen(true)
  }

  const handleSyncData = async (platformId: string) => {
    setIsSyncing(platformId)
    try {
      await axios.post(`/api/integrations/sync/${platformId}`)
      toast.success(`${platformId} data synced successfully`)
      fetchIntegrations()
    } catch (error) {
      toast.error(`Failed to sync ${platformId} data`)
    } finally {
      setIsSyncing(null)
    }
  }

  const isConnected = (platformId: string) => {
    return integrations.some((integration) => integration.platform === platformId && integration.is_active)
  }

  const getLastSync = (platformId: string) => {
    const integration = integrations.find((integration) => integration.platform === platformId)
    return integration?.last_sync
  }

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
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Integrations</h1>
            <p className="text-gray-600 mt-1">Connect your platforms to start syncing data</p>
          </div>
          <button
            onClick={fetchIntegrations}
            disabled={isLoading}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            <RefreshCw size={16} className={isLoading ? "animate-spin" : ""} />
            <span>Refresh</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {availableIntegrations.map((integration, index) => (
            <motion.div
              key={integration.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <IntegrationCard
                integration={integration}
                isConnected={isConnected(integration.id)}
                lastSync={getLastSync(integration.id)}
                onConnect={() => handleConnect(integration.id)}
                onSync={() => handleSyncData(integration.id)}
                isSyncing={isSyncing === integration.id}
              />
            </motion.div>
          ))}
        </div>
      </div>

      <IntegrationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        integration={availableIntegrations.find((i) => i.id === selectedIntegration)}
        onSuccess={() => {
          setIsModalOpen(false)
          fetchIntegrations()
        }}
      />
    </DashboardLayout>
  )
}
