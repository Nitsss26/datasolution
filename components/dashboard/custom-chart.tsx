'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { Settings, Download, Maximize2 } from 'lucide-react'
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
)

interface CustomChartProps {
  type: 'line' | 'bar' | 'pie' | 'area' | 'gauge' | 'funnel' | 'heatmap' | 'scatter' | 'table'
  title: string
  data?: any
  metric?: string
  isLoading?: boolean
  customizable?: boolean
  onCustomize?: () => void
  onExport?: () => void
  onMaximize?: () => void
}

export function CustomChart({
  type,
  title,
  data,
  metric,
  isLoading,
  customizable = false,
  onCustomize,
  onExport,
  onMaximize
}: CustomChartProps) {
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <Skeleton className="h-5 w-32" />
            <Skeleton className="h-8 w-20" />
          </div>
        </CardHeader>
        <CardContent>
          <Skeleton className="h-64 w-full" />
        </CardContent>
      </Card>
    )
  }

  // Generate mock chart data based on type and metric
  const generateChartData = () => {
    const labels = Array.from({ length: 30 }, (_, i) => {
      const date = new Date()
      date.setDate(date.getDate() - (29 - i))
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    })

    const generateValues = (min: number, max: number) => 
      Array.from({ length: 30 }, () => Math.floor(Math.random() * (max - min)) + min)

    switch (type) {
      case 'line':
      case 'area':
        return {
          labels,
          datasets: [
            {
              label: metric || 'Revenue',
              data: generateValues(50000, 150000),
              borderColor: 'rgb(59, 130, 246)',
              backgroundColor: type === 'area' ? 'rgba(59, 130, 246, 0.1)' : 'rgb(59, 130, 246)',
              fill: type === 'area',
              tension: 0.4
            }
          ]
        }

      case 'bar':
        return {
          labels: ['Shopify', 'Facebook Ads', 'Google Ads', 'Shiprocket'],
          datasets: [
            {
              label: metric || 'Revenue',
              data: [2847650, 1423825, 1138706, 285119],
              backgroundColor: [
                'rgba(59, 130, 246, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(245, 158, 11, 0.8)',
                'rgba(239, 68, 68, 0.8)'
              ],
              borderColor: [
                'rgb(59, 130, 246)',
                'rgb(16, 185, 129)',
                'rgb(245, 158, 11)',
                'rgb(239, 68, 68)'
              ],
              borderWidth: 1
            }
          ]
        }

      case 'pie':
        return {
          labels: ['Organic', 'Paid Ads', 'Social Media', 'Direct'],
          datasets: [
            {
              data: [40, 35, 15, 10],
              backgroundColor: [
                'rgba(59, 130, 246, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(245, 158, 11, 0.8)',
                'rgba(239, 68, 68, 0.8)'
              ],
              borderColor: [
                'rgb(59, 130, 246)',
                'rgb(16, 185, 129)',
                'rgb(245, 158, 11)',
                'rgb(239, 68, 68)'
              ],
              borderWidth: 2
            }
          ]
        }

      default:
        return {
          labels,
          datasets: [
            {
              label: metric || 'Data',
              data: generateValues(0, 100),
              borderColor: 'rgb(59, 130, 246)',
              backgroundColor: 'rgba(59, 130, 246, 0.1)'
            }
          ]
        }
    }
  }

  const chartData = generateChartData()

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
      },
    },
    scales: type === 'pie' ? undefined : {
      x: {
        display: true,
        grid: {
          display: false,
        },
      },
      y: {
        display: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
    },
  }

  const renderChart = () => {
    switch (type) {
      case 'line':
      case 'area':
        return <Line data={chartData} options={chartOptions} />
      case 'bar':
        return <Bar data={chartData} options={chartOptions} />
      case 'pie':
        return <Pie data={chartData} options={chartOptions} />
      case 'gauge':
        return (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">
                {data || '4.2x'}
              </div>
              <div className="text-sm text-muted-foreground">
                {metric || 'ROAS'}
              </div>
              <div className="w-32 h-2 bg-gray-200 rounded-full mt-4 mx-auto">
                <div className="w-20 h-2 bg-blue-600 rounded-full"></div>
              </div>
            </div>
          </div>
        )
      case 'funnel':
        return (
          <div className="space-y-2 p-4">
            {[
              { label: 'Impressions', value: '2.1M', width: '100%' },
              { label: 'Clicks', value: '212K', width: '80%' },
              { label: 'Visits', value: '185K', width: '60%' },
              { label: 'Conversions', value: '7.8K', width: '40%' },
              { label: 'Purchases', value: '6.2K', width: '20%' }
            ].map((item, index) => (
              <div key={index} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span>{item.label}</span>
                  <span className="font-medium">{item.value}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-6">
                  <div 
                    className="bg-blue-600 h-6 rounded-full flex items-center justify-center text-white text-xs font-medium"
                    style={{ width: item.width }}
                  >
                    {item.value}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      case 'heatmap':
        return (
          <div className="grid grid-cols-7 gap-1 p-4">
            {Array.from({ length: 35 }, (_, i) => (
              <div
                key={i}
                className={`aspect-square rounded text-xs flex items-center justify-center text-white font-medium ${
                  Math.random() > 0.7 ? 'bg-red-500' :
                  Math.random() > 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                }`}
              >
                {Math.floor(Math.random() * 100)}
              </div>
            ))}
          </div>
        )
      case 'scatter':
        return <Line data={chartData} options={chartOptions} />
      case 'table':
        return (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Platform</th>
                  <th className="text-right p-2">Revenue</th>
                  <th className="text-right p-2">Orders</th>
                  <th className="text-right p-2">AOV</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { platform: 'Shopify', revenue: '₹28,47,651', orders: '8,945', aov: '₹318' },
                  { platform: 'Facebook Ads', revenue: '₹14,23,825', orders: '4,250', aov: '₹335' },
                  { platform: 'Google Ads', revenue: '₹11,38,706', orders: '3,500', aov: '₹325' },
                  { platform: 'Shiprocket', revenue: '₹2,85,119', orders: '1,195', aov: '₹239' }
                ].map((row, index) => (
                  <tr key={index} className="border-b">
                    <td className="p-2 font-medium">{row.platform}</td>
                    <td className="p-2 text-right">{row.revenue}</td>
                    <td className="p-2 text-right">{row.orders}</td>
                    <td className="p-2 text-right">{row.aov}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      default:
        return <Line data={chartData} options={chartOptions} />
    }
  }

  return (
    <Card className="hover:shadow-md transition-all duration-200">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-base font-medium">{title}</CardTitle>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-xs">
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </Badge>
          {customizable && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onCustomize}
              className="h-8 w-8 p-0"
            >
              <Settings className="h-4 w-4" />
            </Button>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={onExport}
            className="h-8 w-8 p-0"
          >
            <Download className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={onMaximize}
            className="h-8 w-8 p-0"
          >
            <Maximize2 className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="h-64">
          {renderChart()}
        </div>
      </CardContent>
    </Card>
  )
}