"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ShoppingBag, Facebook, Search, Truck, Plus, Settings, CheckCircle, AlertCircle, RefreshCw } from "lucide-react"

const integrations = [
  {
    id: "shopify",
    name: "Shopify",
    description: "Connect your Shopify store to sync orders, products, and customer data",
    icon: ShoppingBag,
    color: "bg-green-500",
    fields: [
      { name: "api_key", label: "API Key", type: "password", required: true },
      {
        name: "shop_domain",
        label: "Shop Domain",
        type: "text",
        required: true,
        placeholder: "your-shop.myshopify.com",
      },
    ],
  },
  {
    id: "facebook_ads",
    name: "Facebook Ads",
    description: "Import your Facebook advertising data and campaign performance",
    icon: Facebook,
    color: "bg-blue-600",
    fields: [{ name: "access_token", label: "Access Token", type: "password", required: true }],
  },
  {
    id: "google_ads",
    name: "Google Ads",
    description: "Sync Google Ads campaigns, keywords, and performance metrics",
    icon: Search,
    color: "bg-red-500",
    fields: [
      { name: "access_token", label: "Access Token", type: "password", required: true },
      { name: "customer_id", label: "Customer ID", type: "text", required: true },
      { name: "developer_token", label: "Developer Token", type: "password", required: true },
    ],
  },
  {
    id: "shiprocket",
    name: "Shiprocket",
    description: "Track shipping data, delivery times, and logistics performance",
    icon: Truck,
    color: "bg-orange-500",
    fields: [{ name: "api_key", label: "API Key", type: "password", required: true }],
  },
]

export default function IntegrationsPage() {
  const [connectedIntegrations, setConnectedIntegrations] = useState<string[]>([])
  const [selectedIntegration, setSelectedIntegration] = useState<any>(null)
  const [formData, setFormData] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  useEffect(() => {
    fetchConnectedIntegrations()
  }, [])

  const fetchConnectedIntegrations = async () => {
    try {
      const token = localStorage.getItem("token")
      const response = await fetch("http://localhost:8000/api/integrations/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setConnectedIntegrations(data.map((integration: any) => integration.platform))
      }
    } catch (err) {
      console.error("Failed to fetch integrations:", err)
    }
  }

  const handleConnect = (integration: any) => {
    setSelectedIntegration(integration)
    setFormData({})
    setError("")
    setSuccess("")
    setIsDialogOpen(true)
  }

  const handleFormChange = (field: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")

    try {
      const token = localStorage.getItem("token")
      const response = await fetch("http://localhost:8000/api/integrations/connect", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          platform: selectedIntegration.id,
          api_key: formData.api_key || formData.access_token,
          additional_config: Object.fromEntries(
            Object.entries(formData).filter(([key]) => key !== "api_key" && key !== "access_token"),
          ),
        }),
      })

      if (response.ok) {
        setSuccess(`${selectedIntegration.name} connected successfully!`)
        setConnectedIntegrations((prev) => [
          ...prev.filter((id) => id !== selectedIntegration.id),
          selectedIntegration.id,
        ])
        setTimeout(() => {
          setIsDialogOpen(false)
          setSuccess("")
        }, 2000)
      } else {
        const errorData = await response.json()
        setError(errorData.detail || "Connection failed")
      }
    } catch (err) {
      setError("Network error. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleDisconnect = async (integrationId: string) => {
    try {
      const token = localStorage.getItem("token")
      const response = await fetch(`http://localhost:8000/api/integrations/${integrationId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        setConnectedIntegrations((prev) => prev.filter((id) => id !== integrationId))
      }
    } catch (err) {
      console.error("Failed to disconnect:", err)
    }
  }

  const handleSync = async (integrationId: string) => {
    try {
      const token = localStorage.getItem("token")
      const response = await fetch(`http://localhost:8000/api/integrations/sync/${integrationId}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        alert(`Sync completed! ${data.records} records synced.`)
      }
    } catch (err) {
      console.error("Failed to sync:", err)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6 py-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Integrations</h1>
            <p className="text-gray-600">Connect your platforms to start syncing data</p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        {/* Connected Integrations Summary */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4">Connected Platforms</h2>
          <div className="flex flex-wrap gap-2">
            {connectedIntegrations.length > 0 ? (
              connectedIntegrations.map((integrationId) => {
                const integration = integrations.find((i) => i.id === integrationId)
                return integration ? (
                  <Badge key={integrationId} variant="default" className="flex items-center gap-2">
                    <integration.icon className="h-3 w-3" />
                    {integration.name}
                  </Badge>
                ) : null
              })
            ) : (
              <p className="text-gray-500">No integrations connected yet</p>
            )}
          </div>
        </div>

        {/* Available Integrations */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {integrations.map((integration) => {
            const isConnected = connectedIntegrations.includes(integration.id)
            const IconComponent = integration.icon

            return (
              <Card key={integration.id} className="relative">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className={`p-3 rounded-lg ${integration.color} text-white`}>
                      <IconComponent className="h-6 w-6" />
                    </div>
                    {isConnected && (
                      <Badge variant="default" className="bg-green-100 text-green-800">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Connected
                      </Badge>
                    )}
                  </div>
                  <CardTitle>{integration.name}</CardTitle>
                  <CardDescription>{integration.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2">
                    {isConnected ? (
                      <>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleSync(integration.id)}
                          className="flex-1"
                        >
                          <RefreshCw className="h-4 w-4 mr-2" />
                          Sync Now
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => handleConnect(integration)}>
                          <Settings className="h-4 w-4" />
                        </Button>
                        <Button variant="destructive" size="sm" onClick={() => handleDisconnect(integration.id)}>
                          Disconnect
                        </Button>
                      </>
                    ) : (
                      <Button onClick={() => handleConnect(integration)} className="w-full">
                        <Plus className="h-4 w-4 mr-2" />
                        Connect
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Connection Dialog */}
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Connect {selectedIntegration?.name}</DialogTitle>
              <DialogDescription>
                Enter your {selectedIntegration?.name} credentials to connect your account
              </DialogDescription>
            </DialogHeader>

            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {success && (
                <Alert>
                  <CheckCircle className="h-4 w-4" />
                  <AlertDescription>{success}</AlertDescription>
                </Alert>
              )}

              {selectedIntegration?.fields.map((field: any) => (
                <div key={field.name} className="space-y-2">
                  <Label htmlFor={field.name}>
                    {field.label}
                    {field.required && <span className="text-red-500 ml-1">*</span>}
                  </Label>
                  <Input
                    id={field.name}
                    type={field.type}
                    placeholder={field.placeholder}
                    value={formData[field.name] || ""}
                    onChange={(e) => handleFormChange(field.name, e.target.value)}
                    required={field.required}
                  />
                </div>
              ))}

              <div className="flex gap-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)} className="flex-1">
                  Cancel
                </Button>
                <Button type="submit" disabled={isLoading} className="flex-1">
                  {isLoading ? "Connecting..." : "Connect"}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}
