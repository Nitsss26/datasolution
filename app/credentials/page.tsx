'use client'

import { useState } from 'react'
import { AppHeader } from '@/components/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ShoppingCart, Facebook, Chrome, Truck, CheckCircle, XCircle, Eye, EyeOff } from 'lucide-react'

interface CredentialField {
  key: string
  label: string
  type: 'text' | 'password'
  required: boolean
  placeholder?: string
  description?: string
  value?: string
}

interface PlatformCredentials {
  id: string
  name: string
  icon: any
  connected: boolean
  lastSync?: string
  fields: CredentialField[]
}

export default function CredentialsPage() {
  const [loading, setLoading] = useState(false)
  const [showPasswords, setShowPasswords] = useState<Record<string, boolean>>({})
  const [platforms, setPlatforms] = useState<PlatformCredentials[]>([
    {
      id: 'shopify',
      name: 'Shopify',
      icon: ShoppingCart,
      connected: false,
      fields: [
        {
          key: 'shop_domain',
          label: 'Shop Domain',
          type: 'text',
          required: true,
          placeholder: 'your-shop-name.myshopify.com',
          description: 'Your Shopify store domain'
        },
        {
          key: 'access_token',
          label: 'Access Token',
          type: 'password',
          required: true,
          placeholder: 'shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          description: 'Private app access token from Shopify Admin'
        }
      ]
    },
    {
      id: 'facebook',
      name: 'Facebook Ads',
      icon: Facebook,
      connected: false,
      fields: [
        {
          key: 'access_token',
          label: 'Access Token',
          type: 'password',
          required: true,
          placeholder: 'EAAxxxxxxxxxxxxxxxxxxxxxxxxx',
          description: 'Long-lived access token from Facebook Business'
        },
        {
          key: 'ad_account_id',
          label: 'Ad Account ID',
          type: 'text',
          required: true,
          placeholder: 'act_1234567890',
          description: 'Your Facebook Ad Account ID (with act_ prefix)'
        }
      ]
    },
    {
      id: 'google_ads',
      name: 'Google Ads',
      icon: Chrome,
      connected: false,
      fields: [
        {
          key: 'developer_token',
          label: 'Developer Token',
          type: 'password',
          required: true,
          placeholder: 'xxxxxxxxxxxxxxxxxxxxxxxx',
          description: 'Google Ads API Developer Token'
        },
        {
          key: 'customer_id',
          label: 'Customer ID',
          type: 'text',
          required: true,
          placeholder: '123-456-7890',
          description: 'Google Ads Customer ID'
        }
      ]
    },
    {
      id: 'shiprocket',
      name: 'Shiprocket',
      icon: Truck,
      connected: false,
      fields: [
        {
          key: 'api_key',
          label: 'API Key',
          type: 'password',
          required: true,
          placeholder: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          description: 'Shiprocket API Key from Panel Settings'
        },
        {
          key: 'email',
          label: 'Email',
          type: 'text',
          required: true,
          placeholder: 'your-email@example.com',
          description: 'Shiprocket account email'
        }
      ]
    }
  ])

  const handleSave = async (platformId: string) => {
    setLoading(true)
    try {
      const platform = platforms.find(p => p.id === platformId)
      if (!platform) return

      const credentials = platform.fields.reduce((acc, field) => {
        acc[field.key] = field.value || ''
        return acc
      }, {} as Record<string, string>)

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/credentials/${platformId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      })

      if (response.ok) {
        setPlatforms(prev => prev.map(p => 
          p.id === platformId ? { ...p, connected: true, lastSync: new Date().toISOString() } : p
        ))
        alert('Credentials saved successfully!')
      } else {
        throw new Error('Failed to save credentials')
      }
    } catch (error) {
      alert('Failed to save credentials')
    } finally {
      setLoading(false)
    }
  }

  const togglePasswordVisibility = (fieldKey: string) => {
    setShowPasswords(prev => ({
      ...prev,
      [fieldKey]: !prev[fieldKey]
    }))
  }

  const updateFieldValue = (platformId: string, fieldKey: string, value: string) => {
    setPlatforms(prev => prev.map(platform => 
      platform.id === platformId 
        ? {
            ...platform,
            fields: platform.fields.map(field => 
              field.key === fieldKey ? { ...field, value } : field
            )
          }
        : platform
    ))
  }

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      
      <div className="container mx-auto p-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-6">Platform Credentials</h1>
          
          <Alert className="mb-6">
            <AlertDescription>
              Configure your platform credentials to enable data synchronization. All credentials are encrypted and stored securely.
            </AlertDescription>
          </Alert>

          <Tabs defaultValue="shopify" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              {platforms.map((platform) => {
                const IconComponent = platform.icon
                return (
                  <TabsTrigger key={platform.id} value={platform.id} className="flex items-center gap-2">
                    <IconComponent className="h-4 w-4" />
                    {platform.name}
                    {platform.connected && <CheckCircle className="h-3 w-3 text-green-500" />}
                    {!platform.connected && <XCircle className="h-3 w-3 text-red-500" />}
                  </TabsTrigger>
                )
              })}
            </TabsList>

            {platforms.map((platform) => (
              <TabsContent key={platform.id} value={platform.id}>
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <platform.icon className="h-6 w-6" />
                        <div>
                          <CardTitle>{platform.name}</CardTitle>
                          <CardDescription>
                            Configure your {platform.name} integration
                          </CardDescription>
                        </div>
                      </div>
                      <Badge variant={platform.connected ? "default" : "secondary"}>
                        {platform.connected ? "Connected" : "Not Connected"}
                      </Badge>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="space-y-4">
                    {platform.fields.map((field) => (
                      <div key={field.key} className="space-y-2">
                        <Label htmlFor={field.key}>
                          {field.label}
                          {field.required && <span className="text-red-500 ml-1">*</span>}
                        </Label>
                        
                        <div className="relative">
                          <Input
                            id={field.key}
                            type={field.type === 'password' && !showPasswords[field.key] ? 'password' : 'text'}
                            placeholder={field.placeholder}
                            value={field.value || ''}
                            onChange={(e) => updateFieldValue(platform.id, field.key, e.target.value)}
                            className="pr-10"
                          />
                          
                          {field.type === 'password' && (
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                              onClick={() => togglePasswordVisibility(field.key)}
                            >
                              {showPasswords[field.key] ? (
                                <EyeOff className="h-4 w-4" />
                              ) : (
                                <Eye className="h-4 w-4" />
                              )}
                            </Button>
                          )}
                        </div>
                        
                        {field.description && (
                          <p className="text-sm text-muted-foreground">{field.description}</p>
                        )}
                      </div>
                    ))}
                    
                    <div className="flex justify-end pt-4">
                      <Button 
                        onClick={() => handleSave(platform.id)}
                        disabled={loading}
                      >
                        {loading ? 'Saving...' : 'Save Credentials'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </div>
    </div>
  )
}