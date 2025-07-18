'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import { 
  Search, 
  Filter, 
  Download, 
  TrendingUp, 
  TrendingDown,
  DollarSign,
  Users,
  ShoppingCart,
  Target,
  Truck,
  BarChart3,
  PieChart,
  Activity
} from 'lucide-react'
import type { DashboardData } from '@/types/analytics'

interface ExhaustiveMetricsGridProps {
  data?: DashboardData
  isLoading?: boolean
  platforms: string[]
  timeRange: string
}

interface MetricItem {
  id: string
  category: string
  name: string
  value: string | number
  change: number
  icon: any
  description: string
  format: 'currency' | 'number' | 'percentage' | 'decimal' | 'time'
}

export function ExhaustiveMetricsGrid({ data, isLoading, platforms, timeRange }: ExhaustiveMetricsGridProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <Skeleton className="h-8 w-48" />
          <div className="flex gap-2">
            <Skeleton className="h-10 w-32" />
            <Skeleton className="h-10 w-24" />
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Array.from({ length: 20 }).map((_, i) => (
            <Card key={i}>
              <CardContent className="p-4">
                <Skeleton className="h-4 w-20 mb-2" />
                <Skeleton className="h-8 w-24 mb-1" />
                <Skeleton className="h-3 w-32" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  const formatValue = (value: number | string, format: string) => {
    if (typeof value === 'string') return value

    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('en-IN', { 
          style: 'currency', 
          currency: 'INR',
          maximumFractionDigits: 0
        }).format(value)
      case 'number':
        return new Intl.NumberFormat('en-IN').format(value)
      case 'percentage':
        return `${value.toFixed(2)}%`
      case 'decimal':
        return value.toFixed(2)
      case 'time':
        return `${value.toFixed(1)} days`
      default:
        return value.toString()
    }
  }

  const getTrendIcon = (change: number) => {
    if (change > 0) return <TrendingUp className="h-3 w-3 text-green-500" />
    if (change < 0) return <TrendingDown className="h-3 w-3 text-red-500" />
    return null
  }

  const getTrendColor = (change: number) => {
    if (change > 0) return 'text-green-600'
    if (change < 0) return 'text-red-600'
    return 'text-muted-foreground'
  }

  // Generate comprehensive metrics from data
  const allMetrics: MetricItem[] = [
    // Revenue Metrics
    {
      id: 'total-revenue',
      category: 'Revenue',
      name: 'Total Revenue',
      value: data?.d2cMetrics?.totalRevenue || 2847650.75,
      change: 20.1,
      icon: DollarSign,
      description: 'Total revenue across all platforms',
      format: 'currency'
    },
    {
      id: 'gross-profit',
      category: 'Revenue',
      name: 'Gross Profit',
      value: data?.d2cMetrics?.grossProfit || 1423825.38,
      change: 15.3,
      icon: TrendingUp,
      description: 'Revenue minus cost of goods sold',
      format: 'currency'
    },
    {
      id: 'net-profit',
      category: 'Revenue',
      name: 'Net Profit',
      value: data?.d2cMetrics?.netProfit || 854295.23,
      change: 12.8,
      icon: Target,
      description: 'Profit after all expenses',
      format: 'currency'
    },
    {
      id: 'aov',
      category: 'Revenue',
      name: 'Average Order Value',
      value: data?.d2cMetrics?.averageOrderValue || 318.45,
      change: 5.2,
      icon: BarChart3,
      description: 'Average value per order',
      format: 'currency'
    },
    {
      id: 'gmv',
      category: 'Revenue',
      name: 'Gross Merchandise Value',
      value: data?.d2cMetrics?.grossMerchandiseValue || 2847650.75,
      change: 18.7,
      icon: PieChart,
      description: 'Total value of merchandise sold',
      format: 'currency'
    },

    // Customer Metrics
    {
      id: 'total-customers',
      category: 'Customers',
      name: 'Total Customers',
      value: (data?.d2cMetrics?.newCustomerCount || 1368) + (data?.d2cMetrics?.returningCustomerCount || 2053),
      change: 8.7,
      icon: Users,
      description: 'Total unique customers',
      format: 'number'
    },
    {
      id: 'new-customers',
      category: 'Customers',
      name: 'New Customers',
      value: data?.d2cMetrics?.newCustomerCount || 1368,
      change: 12.4,
      icon: Users,
      description: 'First-time customers',
      format: 'number'
    },
    {
      id: 'returning-customers',
      category: 'Customers',
      name: 'Returning Customers',
      value: data?.d2cMetrics?.returningCustomerCount || 2053,
      change: 6.2,
      icon: Users,
      description: 'Repeat customers',
      format: 'number'
    },
    {
      id: 'cac',
      category: 'Customers',
      name: 'Customer Acquisition Cost',
      value: data?.d2cMetrics?.customerAcquisitionCost || 125.50,
      change: -3.1,
      icon: Target,
      description: 'Cost to acquire a new customer',
      format: 'currency'
    },
    {
      id: 'clv',
      category: 'Customers',
      name: 'Customer Lifetime Value',
      value: data?.d2cMetrics?.customerLifetimeValue || 1250.75,
      change: 18.9,
      icon: Activity,
      description: 'Average customer lifetime value',
      format: 'currency'
    },
    {
      id: 'retention-rate',
      category: 'Customers',
      name: 'Customer Retention Rate',
      value: data?.d2cMetrics?.customerRetentionRate || 91.8,
      change: 2.3,
      icon: Users,
      description: 'Percentage of customers retained',
      format: 'percentage'
    },
    {
      id: 'churn-rate',
      category: 'Customers',
      name: 'Churn Rate',
      value: data?.d2cMetrics?.churnRate || 8.2,
      change: -1.5,
      icon: TrendingDown,
      description: 'Percentage of customers lost',
      format: 'percentage'
    },

    // Order Metrics
    {
      id: 'total-orders',
      category: 'Orders',
      name: 'Total Orders',
      value: data?.d2cMetrics?.totalOrders || 8945,
      change: 12.5,
      icon: ShoppingCart,
      description: 'Total number of orders',
      format: 'number'
    },
    {
      id: 'repeat-purchase-rate',
      category: 'Orders',
      name: 'Repeat Purchase Rate',
      value: data?.d2cMetrics?.repeatPurchaseRate || 35.5,
      change: 4.2,
      icon: ShoppingCart,
      description: 'Percentage of repeat purchases',
      format: 'percentage'
    },

    // Marketing Metrics
    {
      id: 'roas',
      category: 'Marketing',
      name: 'Return on Ad Spend',
      value: data?.adMetrics?.returnOnAdSpend || 6.98,
      change: 3.8,
      icon: Target,
      description: 'Revenue generated per ad dollar spent',
      format: 'decimal'
    },
    {
      id: 'ad-spend',
      category: 'Marketing',
      name: 'Total Ad Spend',
      value: data?.d2cMetrics?.adSpend || 810000.75,
      change: 8.4,
      icon: DollarSign,
      description: 'Total advertising expenditure',
      format: 'currency'
    },
    {
      id: 'impressions',
      category: 'Marketing',
      name: 'Total Impressions',
      value: data?.adMetrics?.impressions || 21250000,
      change: 15.2,
      icon: BarChart3,
      description: 'Total ad impressions',
      format: 'number'
    },
    {
      id: 'clicks',
      category: 'Marketing',
      name: 'Total Clicks',
      value: data?.adMetrics?.clicks || 212500,
      change: 11.7,
      icon: Target,
      description: 'Total ad clicks',
      format: 'number'
    },
    {
      id: 'ctr',
      category: 'Marketing',
      name: 'Click-Through Rate',
      value: data?.adMetrics?.clickThroughRate || 1.0,
      change: -2.1,
      icon: Activity,
      description: 'Percentage of impressions that resulted in clicks',
      format: 'percentage'
    },
    {
      id: 'cpc',
      category: 'Marketing',
      name: 'Cost Per Click',
      value: data?.adMetrics?.costPerClick || 3.81,
      change: -1.8,
      icon: DollarSign,
      description: 'Average cost per click',
      format: 'currency'
    },
    {
      id: 'conversion-rate',
      category: 'Marketing',
      name: 'Conversion Rate',
      value: data?.adMetrics?.conversionRate || 3.65,
      change: -0.8,
      icon: Target,
      description: 'Percentage of clicks that converted',
      format: 'percentage'
    },

    // Operations Metrics
    {
      id: 'avg-delivery-time',
      category: 'Operations',
      name: 'Average Delivery Time',
      value: data?.deliveryMetrics?.avgDeliveryTime || 3.2,
      change: -0.5,
      icon: Truck,
      description: 'Average time to deliver orders',
      format: 'time'
    },
    {
      id: 'on-time-delivery',
      category: 'Operations',
      name: 'On-Time Delivery Rate',
      value: data?.deliveryMetrics?.onTimeDeliveryRate || 92.05,
      change: 1.2,
      icon: Truck,
      description: 'Percentage of on-time deliveries',
      format: 'percentage'
    },
    {
      id: 'shipping-cost',
      category: 'Operations',
      name: 'Total Shipping Cost',
      value: data?.deliveryMetrics?.totalShippingCost || 178900.50,
      change: 5.8,
      icon: DollarSign,
      description: 'Total shipping expenses',
      format: 'currency'
    },
    {
      id: 'return-rate',
      category: 'Operations',
      name: 'Return Rate',
      value: data?.deliveryMetrics?.returnRate || 4.2,
      change: -0.3,
      icon: TrendingDown,
      description: 'Percentage of orders returned',
      format: 'percentage'
    },

    // Website Metrics
    {
      id: 'sessions',
      category: 'Website',
      name: 'Total Sessions',
      value: data?.d2cMetrics?.sessions || 425000,
      change: 22.1,
      icon: BarChart3,
      description: 'Total website sessions',
      format: 'number'
    },
    {
      id: 'bounce-rate',
      category: 'Website',
      name: 'Bounce Rate',
      value: data?.d2cMetrics?.bounceRate || 45.2,
      change: -3.4,
      icon: TrendingDown,
      description: 'Percentage of single-page sessions',
      format: 'percentage'
    },
    {
      id: 'cart-abandonment',
      category: 'Website',
      name: 'Cart Abandonment Rate',
      value: data?.d2cMetrics?.cartAbandonmentRate || 68.5,
      change: -2.1,
      icon: ShoppingCart,
      description: 'Percentage of abandoned carts',
      format: 'percentage'
    }
  ]

  const categories = ['all', ...Array.from(new Set(allMetrics.map(m => m.category)))]

  const filteredMetrics = allMetrics.filter(metric => {
    const matchesSearch = metric.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         metric.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || metric.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Exhaustive Metrics Grid</h2>
          <p className="text-muted-foreground">
            Comprehensive view of all your business metrics across {platforms.includes('all') ? 'all platforms' : `${platforms.length} platform${platforms.length > 1 ? 's' : ''}`}
          </p>
        </div>
        <div className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search metrics..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-64"
            />
          </div>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger className="w-40">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {categories.map(category => (
                <SelectItem key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filteredMetrics.map((metric) => (
          <Card key={metric.id} className="hover:shadow-md transition-all duration-200">
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2">
                <Badge variant="outline" className="text-xs">
                  {metric.category}
                </Badge>
                <metric.icon className="h-4 w-4 text-muted-foreground" />
              </div>
              <div className="space-y-1">
                <h3 className="font-medium text-sm leading-tight">{metric.name}</h3>
                <div className="text-2xl font-bold">
                  {formatValue(metric.value, metric.format)}
                </div>
                <div className="flex items-center gap-1 text-xs">
                  {getTrendIcon(metric.change)}
                  <span className={getTrendColor(metric.change)}>
                    {metric.change > 0 ? '+' : ''}{metric.change}%
                  </span>
                  <span className="text-muted-foreground">vs last period</span>
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  {metric.description}
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredMetrics.length === 0 && (
        <Card>
          <CardContent className="flex items-center justify-center h-32">
            <p className="text-muted-foreground">No metrics found matching your search criteria</p>
          </CardContent>
        </Card>
      )}

      {/* Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Metrics Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">{filteredMetrics.length}</div>
              <div className="text-sm text-muted-foreground">Total Metrics</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600">
                {filteredMetrics.filter(m => m.change > 0).length}
              </div>
              <div className="text-sm text-muted-foreground">Improving</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-red-600">
                {filteredMetrics.filter(m => m.change < 0).length}
              </div>
              <div className="text-sm text-muted-foreground">Declining</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-600">
                {categories.length - 1}
              </div>
              <div className="text-sm text-muted-foreground">Categories</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}