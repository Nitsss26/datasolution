'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { 
  DollarSign, 
  TrendingUp, 
  TrendingDown, 
  Users, 
  ShoppingCart,
  Target,
  Percent,
  Activity,
  Truck,
  CreditCard,
  BarChart3,
  PieChart,
  ArrowUpRight,
  ArrowDownRight,
  Minus
} from 'lucide-react'
import type { DashboardData } from '@/types/analytics'

interface MetricsCardsProps {
  data?: DashboardData
  isLoading?: boolean
}

export function MetricsCards({ data, isLoading }: MetricsCardsProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <Card key={i}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <Skeleton className="h-4 w-20" />
              <Skeleton className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-8 w-24 mb-2" />
              <Skeleton className="h-3 w-32" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (!data) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="flex items-center justify-center h-32">
            <p className="text-muted-foreground">No data available</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  const formatCurrency = (value: number) => 
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)

  const formatNumber = (value: number) => 
    new Intl.NumberFormat('en-US').format(value)

  const formatPercentage = (value: number) => 
    `${value.toFixed(2)}%`

  const getTrendIcon = (trend: number) => {
    if (trend > 0) return <ArrowUpRight className="h-3 w-3 text-green-500" />
    if (trend < 0) return <ArrowDownRight className="h-3 w-3 text-red-500" />
    return <Minus className="h-3 w-3 text-muted-foreground" />
  }

  const getTrendColor = (trend: number) => {
    if (trend > 0) return 'text-green-600'
    if (trend < 0) return 'text-red-600'
    return 'text-muted-foreground'
  }

  const metrics = [
    {
      title: 'Total Revenue',
      value: formatCurrency(data.d2cMetrics?.totalRevenue || 0),
      icon: DollarSign,
      trend: 20.1,
      description: 'vs last month'
    },
    {
      title: 'Gross Profit',
      value: formatCurrency((data.d2cMetrics?.totalRevenue || 0) - (data.d2cMetrics?.costOfGoodsSold || 0)),
      icon: TrendingUp,
      trend: 15.3,
      description: 'vs last month'
    },
    {
      title: 'Total Orders',
      value: formatNumber(data.d2cMetrics?.totalOrders || 0),
      icon: ShoppingCart,
      trend: 12.5,
      description: 'vs last month'
    },
    {
      title: 'New Customers',
      value: formatNumber(data.d2cMetrics?.newCustomerCount || 0),
      icon: Users,
      trend: 8.7,
      description: 'vs last month'
    },
    {
      title: 'Average Order Value',
      value: formatCurrency(data.d2cMetrics?.averageOrderValue || 0),
      icon: BarChart3,
      trend: 5.2,
      description: 'vs last month'
    },
    {
      title: 'Return on Ad Spend',
      value: `${(data.adMetrics?.returnOnAdSpend || 0).toFixed(2)}x`,
      icon: Target,
      trend: 3.8,
      description: 'vs last month'
    },
    {
      title: 'Conversion Rate',
      value: formatPercentage(data.adMetrics?.conversionRate || 0),
      icon: Percent,
      trend: -2.1,
      description: 'vs last month'
    },
    {
      title: 'Customer Lifetime Value',
      value: formatCurrency(data.d2cMetrics?.customerLifetimeValue || 0),
      icon: Activity,
      trend: 18.9,
      description: 'vs last month'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <Card key={index} className="hover:shadow-md transition-all duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {metric.title}
            </CardTitle>
            <metric.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-1">
              {metric.value}
            </div>
            <div className="flex items-center gap-1 text-xs">
              {getTrendIcon(metric.trend)}
              <span className={getTrendColor(metric.trend)}>
                {metric.trend > 0 ? '+' : ''}{metric.trend}%
              </span>
              <span className="text-muted-foreground">
                {metric.description}
              </span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}