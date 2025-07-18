'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { 
  CheckCircle, 
  XCircle, 
  Settings, 
  RefreshCw,
  ExternalLink,
  Key,
  Database,
  Zap
} from 'lucide-react'

interface Platform {
  id: string
  name: string
  description: string
  connected: boolean
  lastSync?: string
  dataPoints?: number
  status: 'connected' | 'disconnected' | 'error' | 'syncing'
  icon: string
  setupUrl?: string
}

export default function IntegrationsPage() {
  const [platforms, setPlatforms] = useState<Platform[]>([
    {
      id: 'shopify',
      name: 'Shopify',
      description: 'Connect your Shopify store to sync orders, customers, and product data',
      connected: true,
      lastSync: '2 minutes ago',
      dataPoints: 1250,
      status: 'connected',
      icon: '🛍️',
      setupUrl: 'https://shopify.com/admin/apps'
    },
    {
      id: 'facebook',
      name: 'Facebook Ads',
      description: 'Import campaign performance, audience insights, and ad spend data',
      connected: true,
      lastSync: '5 minutes ago',
      dataPoints: 850,
      status: 'connected',
      icon: '📘'
    },
    {
      id: 'google',
      name: 'Google Ads',
      description: 'Track keywords, campaigns, and conversion performance',
      connected: true,
      lastSync: '10 minutes ago',
      dataPoints: 650,
      status: 'connected',
      icon: '🎯'
    },
    {
      id: 'shiprocket',
      name: 'Shiprocket',
      description: 'Monitor shipping costs, delivery performance, and tracking data',
      connected: true,
      lastSync: '3 minutes ago',
      dataPoints: 445,
      status: 'connected',
      icon: '🚚'
    },
    {
      id: 'amazon',
      name: 'Amazon Seller Central',
      description: 'Sync Amazon marketplace orders and performance metrics',
      connected: false,
      status: 'disconnected',
      icon: '📦'
    },
    {
      id: 'flipkart',
      name: 'Flipkart Seller Hub',
      description: 'Import Flipkart orders, returns, and marketplace analytics',
      connected: false,
      status: 'disconnected',
      icon: '🛒'
    }
  ])

  const [isLoading, setIsLoading] = useState(false)

  const handleConnect = async (platformId: string) => {
    setIsLoading(true)
    // Simulate API call
    setTimeout(() => {
      setPlatforms(prev => prev.map(p => 
        p.id === platformId 
          ? { ...p, connected: true, status: 'connected' as const, lastSync: 'Just now', dataPoints: 0 }
          : p
      ))
      setIsLoading(false)
    }, 2000)
  }

  const handleDisconnect = async (platformId: string) => {
    setPlatforms(prev => prev.map(p => 
      p.id === platformId 
        ? { ...p, connected: false, status: 'disconnected' as const, lastSync: undefined, dataPoints: 0 }
        : p
    ))
  }

  const handleSync = async (platformId: string) => {
    setPlatforms(prev => prev.map(p => 
      p.id === platformId 
        ? { ...p, status: 'syncing' as const }
        : p
    ))

    // Simulate sync
    setTimeout(() => {
      setPlatforms(prev => prev.map(p => 
        p.id === platformId 
          ? { ...p, status: 'connected' as const, lastSync: 'Just now' }
          : p
      ))
    }, 3000)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'syncing':
        return <RefreshCw className="h-5 w-5 text-blue-500 animate-spin" />
      case 'error':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <XCircle className="h-5 w-5 text-gray-400" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'connected':
        return <Badge className="bg-green-100 text-green-800">Connected</Badge>
      case 'syncing':
        return <Badge className="bg-blue-100 text-blue-800">Syncing...</Badge>
      case 'error':
        return <Badge variant="destructive">Error</Badge>
      default:
        return <Badge variant="secondary">Not Connected</Badge>
    }
  }

  const connectedPlatforms = platforms.filter(p => p.connected).length
  const totalDataPoints = platforms.reduce((sum, p) => sum + (p.dataPoints || 0), 0)

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Platform Integrations</h1>
              <p className="text-muted-foreground mt-1">
                Connect your business platforms to unlock comprehensive analytics
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{connectedPlatforms}</div>
                <div className="text-sm text-muted-foreground">Connected</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{totalDataPoints.toLocaleString()}</div>
                <div className="text-sm text-muted-foreground">Data Points</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="space-y-6">
          {/* Overview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardContent className="flex items-center gap-4 p-6">
                <div className="p-3 bg-green-100 rounded-full">
                  <Database className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <div className="text-2xl font-bold">{connectedPlatforms}/6</div>
                  <div className="text-sm text-muted-foreground">Platforms Connected</div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="flex items-center gap-4 p-6">
                <div className="p-3 bg-blue-100 rounded-full">
                  <Zap className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <div className="text-2xl font-bold">{totalDataPoints.toLocaleString()}</div>
                  <div className="text-sm text-muted-foreground">Total Data Points</div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="flex items-center gap-4 p-6">
                <div className="p-3 bg-purple-100 rounded-full">
                  <RefreshCw className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <div className="text-2xl font-bold">Real-time</div>
                  <div className="text-sm text-muted-foreground">Data Sync</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Platform Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {platforms.map((platform) => (
              <Card key={platform.id} className="hover:shadow-md transition-all duration-200">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="text-2xl">{platform.icon}</div>
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          {platform.name}
                          {getStatusIcon(platform.status)}
                        </CardTitle>
                        <p className="text-sm text-muted-foreground mt-1">
                          {platform.description}
                        </p>
                      </div>
                    </div>
                    {getStatusBadge(platform.status)}
                  </div>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  {platform.connected && (
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <Label className="text-muted-foreground">Last Sync</Label>
                        <div className="font-medium">{platform.lastSync}</div>
                      </div>
                      <div>
                        <Label className="text-muted-foreground">Data Points</Label>
                        <div className="font-medium">{platform.dataPoints?.toLocaleString()}</div>
                      </div>
                    </div>
                  )}
                  
                  <Separator />
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {platform.setupUrl && (
                        <Button variant="outline" size="sm" asChild>
                          <a href={platform.setupUrl} target="_blank" rel="noopener noreferrer">
                            <ExternalLink className="h-4 w-4 mr-2" />
                            Setup Guide
                          </a>
                        </Button>
                      )}
                      {platform.connected && (
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => handleSync(platform.id)}
                          disabled={platform.status === 'syncing'}
                        >
                          <RefreshCw className={`h-4 w-4 mr-2 ${platform.status === 'syncing' ? 'animate-spin' : ''}`} />
                          Sync Now
                        </Button>
                      )}
                    </div>
                    
                    <div className="flex items-center gap-2">
                      {platform.connected ? (
                        <>
                          <Button variant="outline" size="sm">
                            <Settings className="h-4 w-4 mr-2" />
                            Configure
                          </Button>
                          <Button 
                            variant="destructive" 
                            size="sm"
                            onClick={() => handleDisconnect(platform.id)}
                          >
                            Disconnect
                          </Button>
                        </>
                      ) : (
                        <Button 
                          onClick={() => handleConnect(platform.id)}
                          disabled={isLoading}
                          size="sm"
                        >
                          <Key className="h-4 w-4 mr-2" />
                          Connect
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Setup Instructions */}
          <Card>
            <CardHeader>
              <CardTitle>Integration Setup Guide</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium mb-2">🔑 API Keys Required</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Shopify: Admin API access token</li>
                    <li>• Facebook Ads: Business Manager token</li>
                    <li>• Google Ads: Developer token + OAuth</li>
                    <li>• Shiprocket: API credentials</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium mb-2">📊 Data Synced</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Orders, customers, products</li>
                    <li>• Campaign performance metrics</li>
                    <li>• Shipping and delivery data</li>
                    <li>• Revenue and cost analytics</li>
                  </ul>
                </div>
              </div>
              
              <Separator />
              
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-2">💡 Pro Tip</h4>
                <p className="text-sm text-blue-700">
                  The platform works perfectly in demo mode without any API keys. 
                  Connect your platforms when you're ready to analyze real data!
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}