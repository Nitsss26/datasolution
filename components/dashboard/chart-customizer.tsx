'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { Badge } from '@/components/ui/badge'
import { Plus, BarChart3, LineChart, PieChart, Activity } from 'lucide-react'
import type { ChartConfig } from '@/types/analytics'

interface ChartCustomizerProps {
  onAddChart: (config: ChartConfig) => void
}

const CHART_TYPES = [
  { value: 'line', label: 'Line Chart', icon: LineChart },
  { value: 'bar', label: 'Bar Chart', icon: BarChart3 },
  { value: 'pie', label: 'Pie Chart', icon: PieChart },
  { value: 'area', label: 'Area Chart', icon: Activity },
  { value: 'gauge', label: 'Gauge Chart', icon: Activity },
  { value: 'funnel', label: 'Funnel Chart', icon: Activity },
  { value: 'heatmap', label: 'Heatmap', icon: Activity },
  { value: 'scatter', label: 'Scatter Plot', icon: Activity },
  { value: 'table', label: 'Data Table', icon: Activity }
]

const METRICS = [
  { value: 'totalRevenue', label: 'Total Revenue', category: 'Revenue' },
  { value: 'grossProfit', label: 'Gross Profit', category: 'Revenue' },
  { value: 'netProfit', label: 'Net Profit', category: 'Revenue' },
  { value: 'averageOrderValue', label: 'Average Order Value', category: 'Revenue' },
  { value: 'totalOrders', label: 'Total Orders', category: 'Orders' },
  { value: 'newCustomerCount', label: 'New Customers', category: 'Customers' },
  { value: 'returningCustomerCount', label: 'Returning Customers', category: 'Customers' },
  { value: 'customerAcquisitionCost', label: 'Customer Acquisition Cost', category: 'Customers' },
  { value: 'customerLifetimeValue', label: 'Customer Lifetime Value', category: 'Customers' },
  { value: 'returnOnAdSpend', label: 'Return on Ad Spend', category: 'Marketing' },
  { value: 'adSpend', label: 'Ad Spend', category: 'Marketing' },
  { value: 'impressions', label: 'Impressions', category: 'Marketing' },
  { value: 'clicks', label: 'Clicks', category: 'Marketing' },
  { value: 'clickThroughRate', label: 'Click-Through Rate', category: 'Marketing' },
  { value: 'conversionRate', label: 'Conversion Rate', category: 'Marketing' },
  { value: 'avgDeliveryTime', label: 'Average Delivery Time', category: 'Operations' },
  { value: 'onTimeDeliveryRate', label: 'On-Time Delivery Rate', category: 'Operations' },
  { value: 'shippingCosts', label: 'Shipping Costs', category: 'Operations' },
  { value: 'returnRate', label: 'Return Rate', category: 'Operations' },
  { value: 'sessions', label: 'Website Sessions', category: 'Website' },
  { value: 'bounceRate', label: 'Bounce Rate', category: 'Website' },
  { value: 'cartAbandonmentRate', label: 'Cart Abandonment Rate', category: 'Website' }
]

const TIME_RANGES = [
  { value: '7d', label: 'Last 7 days' },
  { value: '30d', label: 'Last 30 days' },
  { value: '90d', label: 'Last 90 days' },
  { value: '6m', label: 'Last 6 months' },
  { value: '1y', label: 'Last year' }
]

export function ChartCustomizer({ onAddChart }: ChartCustomizerProps) {
  const [config, setConfig] = useState<ChartConfig>({
    type: 'line',
    title: '',
    metric: '',
    timeRange: '30d',
    options: {
      showLegend: true,
      showGrid: true,
      showLabels: true
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!config.title || !config.metric) {
      return
    }

    onAddChart({
      ...config,
      id: Date.now().toString()
    })

    // Reset form
    setConfig({
      type: 'line',
      title: '',
      metric: '',
      timeRange: '30d',
      options: {
        showLegend: true,
        showGrid: true,
        showLabels: true
      }
    })
  }

  const selectedChartType = CHART_TYPES.find(type => type.value === config.type)
  const selectedMetric = METRICS.find(metric => metric.value === config.metric)

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Plus className="h-5 w-5" />
          Chart Customizer
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Chart Type Selection */}
          <div className="space-y-3">
            <Label>Chart Type</Label>
            <div className="grid grid-cols-3 gap-2">
              {CHART_TYPES.map((type) => (
                <Button
                  key={type.value}
                  type="button"
                  variant={config.type === type.value ? "default" : "outline"}
                  size="sm"
                  onClick={() => setConfig(prev => ({ ...prev, type: type.value as any }))}
                  className="flex flex-col items-center gap-1 h-auto py-3"
                >
                  <type.icon className="h-4 w-4" />
                  <span className="text-xs">{type.label}</span>
                </Button>
              ))}
            </div>
            {selectedChartType && (
              <Badge variant="outline" className="text-xs">
                Selected: {selectedChartType.label}
              </Badge>
            )}
          </div>

          {/* Chart Title */}
          <div className="space-y-2">
            <Label htmlFor="title">Chart Title</Label>
            <Input
              id="title"
              placeholder="Enter chart title..."
              value={config.title}
              onChange={(e) => setConfig(prev => ({ ...prev, title: e.target.value }))}
              required
            />
          </div>

          {/* Metric Selection */}
          <div className="space-y-2">
            <Label>Primary Metric</Label>
            <Select 
              value={config.metric} 
              onValueChange={(value) => setConfig(prev => ({ ...prev, metric: value }))}
              required
            >
              <SelectTrigger>
                <SelectValue placeholder="Select a metric..." />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(
                  METRICS.reduce((acc, metric) => {
                    if (!acc[metric.category]) acc[metric.category] = []
                    acc[metric.category].push(metric)
                    return acc
                  }, {} as Record<string, typeof METRICS>)
                ).map(([category, metrics]) => (
                  <div key={category}>
                    <div className="px-2 py-1 text-xs font-medium text-muted-foreground">
                      {category}
                    </div>
                    {metrics.map((metric) => (
                      <SelectItem key={metric.value} value={metric.value}>
                        {metric.label}
                      </SelectItem>
                    ))}
                  </div>
                ))}
              </SelectContent>
            </Select>
            {selectedMetric && (
              <Badge variant="secondary" className="text-xs">
                {selectedMetric.category}: {selectedMetric.label}
              </Badge>
            )}
          </div>

          {/* Time Range */}
          <div className="space-y-2">
            <Label>Time Range</Label>
            <Select 
              value={config.timeRange} 
              onValueChange={(value) => setConfig(prev => ({ ...prev, timeRange: value }))}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {TIME_RANGES.map((range) => (
                  <SelectItem key={range.value} value={range.value}>
                    {range.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Chart Options */}
          <div className="space-y-3">
            <Label>Chart Options</Label>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="showLegend"
                  checked={config.options?.showLegend}
                  onCheckedChange={(checked) => 
                    setConfig(prev => ({
                      ...prev,
                      options: { ...prev.options, showLegend: checked as boolean }
                    }))
                  }
                />
                <Label htmlFor="showLegend" className="text-sm">Show Legend</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="showGrid"
                  checked={config.options?.showGrid}
                  onCheckedChange={(checked) => 
                    setConfig(prev => ({
                      ...prev,
                      options: { ...prev.options, showGrid: checked as boolean }
                    }))
                  }
                />
                <Label htmlFor="showGrid" className="text-sm">Show Grid Lines</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="showLabels"
                  checked={config.options?.showLabels}
                  onCheckedChange={(checked) => 
                    setConfig(prev => ({
                      ...prev,
                      options: { ...prev.options, showLabels: checked as boolean }
                    }))
                  }
                />
                <Label htmlFor="showLabels" className="text-sm">Show Data Labels</Label>
              </div>
            </div>
          </div>

          {/* Preview */}
          <div className="space-y-2">
            <Label>Preview</Label>
            <div className="p-4 border rounded-lg bg-muted/50">
              <div className="text-sm font-medium mb-2">
                {config.title || 'Chart Title'}
              </div>
              <div className="text-xs text-muted-foreground">
                {selectedChartType?.label} • {selectedMetric?.label} • {TIME_RANGES.find(r => r.value === config.timeRange)?.label}
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <Button 
            type="submit" 
            className="w-full"
            disabled={!config.title || !config.metric}
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Custom Chart
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}