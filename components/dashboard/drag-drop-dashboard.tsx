'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  GripVertical, 
  Settings, 
  X, 
  Plus,
  Save,
  RotateCcw
} from 'lucide-react'
import { MetricsCards } from './metrics-cards'
import { CustomChart } from './custom-chart'
import type { DashboardData } from '@/types/analytics'

interface DragDropDashboardProps {
  data?: DashboardData
  isLoading?: boolean
  onSaveLayout: (layout: any[]) => void
}

interface DashboardWidget {
  id: string
  type: 'metrics-cards' | 'chart' | 'custom'
  title: string
  config?: any
  position: { x: number; y: number; w: number; h: number }
}

export function DragDropDashboard({ data, isLoading, onSaveLayout }: DragDropDashboardProps) {
  const [widgets, setWidgets] = useState<DashboardWidget[]>([
    {
      id: 'metrics-1',
      type: 'metrics-cards',
      title: 'Key Metrics Overview',
      position: { x: 0, y: 0, w: 12, h: 2 }
    },
    {
      id: 'chart-1',
      type: 'chart',
      title: 'Revenue Trend',
      config: { type: 'line', metric: 'totalRevenue' },
      position: { x: 0, y: 2, w: 6, h: 4 }
    },
    {
      id: 'chart-2',
      type: 'chart',
      title: 'Platform Performance',
      config: { type: 'bar', metric: 'revenue' },
      position: { x: 6, y: 2, w: 6, h: 4 }
    },
    {
      id: 'chart-3',
      type: 'chart',
      title: 'Revenue Distribution',
      config: { type: 'pie', metric: 'revenuePerChannel' },
      position: { x: 0, y: 6, w: 4, h: 4 }
    },
    {
      id: 'chart-4',
      type: 'chart',
      title: 'ROAS Gauge',
      config: { type: 'gauge', metric: 'returnOnAdSpend' },
      position: { x: 4, y: 6, w: 4, h: 4 }
    },
    {
      id: 'chart-5',
      type: 'chart',
      title: 'Customer Growth',
      config: { type: 'area', metric: 'newCustomerCount' },
      position: { x: 8, y: 6, w: 4, h: 4 }
    }
  ])

  const [draggedWidget, setDraggedWidget] = useState<string | null>(null)
  const [hasChanges, setHasChanges] = useState(false)

  const handleDragStart = (e: React.DragEvent, widgetId: string) => {
    setDraggedWidget(widgetId)
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleDrop = (e: React.DragEvent, targetWidgetId: string) => {
    e.preventDefault()
    
    if (!draggedWidget || draggedWidget === targetWidgetId) return

    const draggedIndex = widgets.findIndex(w => w.id === draggedWidget)
    const targetIndex = widgets.findIndex(w => w.id === targetWidgetId)

    if (draggedIndex === -1 || targetIndex === -1) return

    const newWidgets = [...widgets]
    const [draggedItem] = newWidgets.splice(draggedIndex, 1)
    newWidgets.splice(targetIndex, 0, draggedItem)

    setWidgets(newWidgets)
    setDraggedWidget(null)
    setHasChanges(true)
  }

  const handleRemoveWidget = (widgetId: string) => {
    setWidgets(prev => prev.filter(w => w.id !== widgetId))
    setHasChanges(true)
  }

  const handleSaveLayout = () => {
    onSaveLayout(widgets)
    setHasChanges(false)
  }

  const handleResetLayout = () => {
    // Reset to default layout
    setWidgets([
      {
        id: 'metrics-1',
        type: 'metrics-cards',
        title: 'Key Metrics Overview',
        position: { x: 0, y: 0, w: 12, h: 2 }
      },
      {
        id: 'chart-1',
        type: 'chart',
        title: 'Revenue Trend',
        config: { type: 'line', metric: 'totalRevenue' },
        position: { x: 0, y: 2, w: 6, h: 4 }
      },
      {
        id: 'chart-2',
        type: 'chart',
        title: 'Platform Performance',
        config: { type: 'bar', metric: 'revenue' },
        position: { x: 6, y: 2, w: 6, h: 4 }
      }
    ])
    setHasChanges(true)
  }

  const renderWidget = (widget: DashboardWidget) => {
    switch (widget.type) {
      case 'metrics-cards':
        return <MetricsCards data={data} isLoading={isLoading} />
      
      case 'chart':
        return (
          <CustomChart
            type={widget.config?.type || 'line'}
            title={widget.title}
            data={data}
            metric={widget.config?.metric}
            isLoading={isLoading}
            customizable={true}
          />
        )
      
      default:
        return (
          <Card>
            <CardContent className="flex items-center justify-center h-32">
              <p className="text-muted-foreground">Unknown widget type</p>
            </CardContent>
          </Card>
        )
    }
  }

  return (
    <div className="space-y-6">
      {/* Edit Mode Header */}
      <Card className="border-dashed border-2 border-primary/50 bg-primary/5">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Badge variant="default" className="animate-pulse">
                Edit Mode
              </Badge>
              <span className="text-sm text-muted-foreground">
                Drag and drop widgets to customize your dashboard layout
              </span>
            </div>
            <div className="flex items-center gap-2">
              {hasChanges && (
                <Badge variant="outline" className="text-orange-600 border-orange-600">
                  Unsaved Changes
                </Badge>
              )}
              <Button variant="outline" size="sm" onClick={handleResetLayout}>
                <RotateCcw className="h-4 w-4 mr-2" />
                Reset
              </Button>
              <Button size="sm" onClick={handleSaveLayout} disabled={!hasChanges}>
                <Save className="h-4 w-4 mr-2" />
                Save Layout
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Dashboard Grid */}
      <div className="grid grid-cols-12 gap-4 min-h-[600px]">
        {widgets.map((widget) => (
          <div
            key={widget.id}
            className={`col-span-${widget.position.w} relative group`}
            draggable
            onDragStart={(e) => handleDragStart(e, widget.id)}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, widget.id)}
          >
            {/* Widget Controls */}
            <div className="absolute top-2 right-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="flex items-center gap-1 bg-background/90 backdrop-blur-sm rounded-md p-1 shadow-md">
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0 cursor-grab active:cursor-grabbing"
                >
                  <GripVertical className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0"
                >
                  <Settings className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0 text-red-500 hover:text-red-600"
                  onClick={() => handleRemoveWidget(widget.id)}
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            </div>

            {/* Widget Content */}
            <div className={`h-full ${draggedWidget === widget.id ? 'opacity-50' : ''}`}>
              {renderWidget(widget)}
            </div>

            {/* Drop Zone Indicator */}
            <div className="absolute inset-0 border-2 border-dashed border-primary/50 bg-primary/10 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none rounded-lg" />
          </div>
        ))}

        {/* Add Widget Placeholder */}
        <div className="col-span-4">
          <Card className="border-dashed border-2 border-muted-foreground/25 hover:border-primary/50 transition-colors cursor-pointer h-full min-h-[200px]">
            <CardContent className="flex flex-col items-center justify-center h-full text-center p-6">
              <Plus className="h-8 w-8 text-muted-foreground mb-2" />
              <h3 className="font-medium text-muted-foreground mb-1">Add Widget</h3>
              <p className="text-sm text-muted-foreground">
                Click to add a new chart or metric widget
              </p>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Layout Instructions */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Layout Instructions</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground space-y-2">
          <ul className="list-disc list-inside space-y-1">
            <li>Drag widgets by clicking and holding the grip handle (⋮⋮)</li>
            <li>Drop widgets on other widgets to reorder them</li>
            <li>Use the settings button to customize widget properties</li>
            <li>Remove widgets using the X button</li>
            <li>Save your layout when you're satisfied with the arrangement</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}