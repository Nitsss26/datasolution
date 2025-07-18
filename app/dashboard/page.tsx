'use client'

import { useState, useEffect } from 'react'
import { AppHeader } from '@/components/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Users, 
  ShoppingCart, 
  Truck,
  BarChart3,
  PieChart,
  LineChart,
  Settings,
  Download,
  Sparkles,
  RefreshCw,
  Filter,
  Calendar,
  Eye,
  EyeOff,
  Moon,
  Sun,
  Palette,
  Grid3X3,
  Maximize2,
  Plus
} from 'lucide-react'
import { MetricsCards } from '@/components/dashboard/metrics-cards'
import { CustomChart } from '@/components/dashboard/custom-chart'
import { PlatformSelector } from '@/components/dashboard/platform-selector'
import { AIAssistant } from '@/components/dashboard/ai-assistant'
import { PLReport } from '@/components/dashboard/pl-report'
import { ChartCustomizer } from '@/components/dashboard/chart-customizer'
import { ExhaustiveMetricsGrid } from '@/components/dashboard/exhaustive-metrics-grid'
import { DragDropDashboard } from '@/components/dashboard/drag-drop-dashboard'
import { ThemeCustomizer } from '@/components/dashboard/theme-customizer'
import { useAnalytics } from '@/hooks/use-analytics'
import { usePlatforms } from '@/hooks/use-platforms'
import { useAI } from '@/hooks/use-ai'
import { useTheme } from 'next-themes'
import type { ChartConfig, UserPreferences } from '@/types/analytics'

export default function Dashboard() {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['all'])
  const [timeRange, setTimeRange] = useState('30d')
  const [activeTab, setActiveTab] = useState('overview')
  const [showAI, setShowAI] = useState(true)
  const [customCharts, setCustomCharts] = useState<ChartConfig[]>([])
  const [isDragMode, setIsDragMode] = useState(false)
  const [showThemeCustomizer, setShowThemeCustomizer] = useState(false)
  const [demoMode, setDemoMode] = useState(true)
  const [pipelineStatus, setPipelineStatus] = useState<any>(null)
  const [userPrefs, setUserPrefs] = useState<UserPreferences>({
    selectedPlatforms: ['all'],
    defaultTimeRange: '30d',
    favoriteCharts: [],
    theme: 'system',
    aiEnabled: true
  })

  const { theme, setTheme } = useTheme()
  const { data: analyticsData, isLoading, refetch } = useAnalytics({
    platforms: selectedPlatforms,
    timeRange,
    demoMode
  })

  const { platforms } = usePlatforms()
  const { askAI, isProcessing } = useAI()

  // Fetch pipeline status
  useEffect(() => {
    const fetchPipelineStatus = async () => {
      try {
        const response = await fetch('/api/pipeline/status')
        if (response.ok) {
          const status = await response.json()
          setPipelineStatus(status)
        }
      } catch (error) {
        console.error('Failed to fetch pipeline status:', error)
      }
    }

    fetchPipelineStatus()
    const interval = setInterval(fetchPipelineStatus, 30000) // Update every 30 seconds

    return () => clearInterval(interval)
  }, [])

  // Handle demo mode change
  useEffect(() => {
    if (demoMode) {
      // Switch to demo data
      refetch()
    } else {
      // Switch to live data
      refetch()
    }
  }, [demoMode, refetch])

  const handlePlatformChange = (platforms: string[]) => {
    setSelectedPlatforms(platforms)
    setUserPrefs(prev => ({ ...prev, selectedPlatforms: platforms }))
  }

  const handleTimeRangeChange = (range: string) => {
    setTimeRange(range)
    setUserPrefs(prev => ({ ...prev, defaultTimeRange: range }))
  }

  const handleAddCustomChart = (config: ChartConfig) => {
    setCustomCharts(prev => [...prev, config])
  }

  const handleExportPL = async () => {
    if (!analyticsData) return
    
    const response = await fetch('/api/export/pl', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        data: analyticsData,
        platforms: selectedPlatforms,
        timeRange
      })
    })
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `pl-report-${new Date().toISOString().split('T')[0]}.pdf`
    a.click()
  }

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  return (
    <div className="min-h-screen bg-background transition-colors duration-300">
      <AppHeader />
      {/* Enhanced Header with Theme Controls */}
      <div className="border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                D2C Analytics Pro
              </h1>
              <p className="text-muted-foreground">Complete business intelligence platform with AI-powered insights</p>
            </div>
            <div className="flex items-center gap-2">
              {/* Demo Mode Toggle */}
              <div className="flex items-center gap-2 px-3 py-1 border rounded-lg bg-muted/50">
                <Label htmlFor="demo-toggle" className="text-sm">Demo Mode</Label>
                <Switch
                  id="demo-toggle"
                  checked={demoMode}
                  onCheckedChange={setDemoMode}
                />
                <Badge variant={demoMode ? "secondary" : "default"} className="text-xs">
                  {demoMode ? "Dummy Data" : "Live Data"}
                </Badge>
              </div>

              {/* Pipeline Status */}
              {pipelineStatus && (
                <Badge 
                  variant={pipelineStatus.status === 'running' ? "default" : "secondary"}
                  className="animate-pulse"
                >
                  Pipeline: {pipelineStatus.status}
                </Badge>
              )}

              {/* Theme Toggle */}
              <Button
                variant="outline"
                size="sm"
                onClick={toggleTheme}
                className="relative"
              >
                <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                <span className="sr-only">Toggle theme</span>
              </Button>
              
              {/* Theme Customizer */}
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowThemeCustomizer(!showThemeCustomizer)}
              >
                <Palette className="h-4 w-4 mr-2" />
                Customize
              </Button>
              
              {/* Drag Mode Toggle */}
              <Button
                variant={isDragMode ? "default" : "outline"}
                size="sm"
                onClick={() => setIsDragMode(!isDragMode)}
              >
                <Grid3X3 className="h-4 w-4 mr-2" />
                {isDragMode ? 'Exit Edit' : 'Edit Layout'}
              </Button>
              
              {/* Refresh */}
              <Button
                variant="outline"
                size="sm"
                onClick={() => refetch()}
                disabled={isLoading}
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              
              {/* AI Toggle */}
              <Button
                variant={showAI ? "default" : "outline"}
                size="sm"
                onClick={() => setShowAI(!showAI)}
              >
                <Sparkles className="h-4 w-4 mr-2" />
                AI Assistant
              </Button>
              
              {/* Export P&L */}
              <Button onClick={handleExportPL} size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export P&L
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Theme Customizer Panel */}
      {showThemeCustomizer && (
        <div className="border-b bg-muted/50">
          <div className="container mx-auto px-4 py-4">
            <ThemeCustomizer onClose={() => setShowThemeCustomizer(false)} />
          </div>
        </div>
      )}

      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {/* Enhanced Platform & Time Controls */}
            <Card className="border-2 border-dashed border-muted-foreground/25 hover:border-primary/50 transition-colors">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2">
                    <Filter className="h-5 w-5 text-primary" />
                    Advanced Data Filters
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    {platforms.map(platform => (
                      <Badge 
                        key={platform.id}
                        variant={platform.connected ? "default" : "secondary"}
                        className="animate-pulse"
                      >
                        {platform.name}
                        {platform.connected && (
                          <div className="ml-1 h-2 w-2 bg-green-500 rounded-full animate-pulse" />
                        )}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label>Select Platforms</Label>
                    <PlatformSelector
                      platforms={platforms}
                      selected={selectedPlatforms}
                      onChange={handlePlatformChange}
                    />
                  </div>
                  <div>
                    <Label>Time Range</Label>
                    <Select value={timeRange} onValueChange={handleTimeRangeChange}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1d">Last 24 hours</SelectItem>
                        <SelectItem value="7d">Last 7 days</SelectItem>
                        <SelectItem value="30d">Last 30 days</SelectItem>
                        <SelectItem value="90d">Last 90 days</SelectItem>
                        <SelectItem value="6m">Last 6 months</SelectItem>
                        <SelectItem value="1y">Last year</SelectItem>
                        <SelectItem value="custom">Custom range</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Data Granularity</Label>
                    <Select defaultValue="daily">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="hourly">Hourly</SelectItem>
                        <SelectItem value="daily">Daily</SelectItem>
                        <SelectItem value="weekly">Weekly</SelectItem>
                        <SelectItem value="monthly">Monthly</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Enhanced Dashboard Tabs */}
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="grid w-full grid-cols-6 h-12">
                <TabsTrigger value="overview" className="text-sm">Overview</TabsTrigger>
                <TabsTrigger value="exhaustive" className="text-sm">All Metrics</TabsTrigger>
                <TabsTrigger value="revenue" className="text-sm">Revenue</TabsTrigger>
                <TabsTrigger value="marketing" className="text-sm">Marketing</TabsTrigger>
                <TabsTrigger value="operations" className="text-sm">Operations</TabsTrigger>
                <TabsTrigger value="custom" className="text-sm">Custom</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                {isDragMode ? (
                  <DragDropDashboard 
                    data={analyticsData} 
                    isLoading={isLoading}
                    onSaveLayout={(layout) => console.log('Layout saved:', layout)}
                  />
                ) : (
                  <>
                    <MetricsCards data={analyticsData} isLoading={isLoading} />
                    
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      <CustomChart
                        type="line"
                        title="Revenue Trend Analysis"
                        data={analyticsData?.timeSeriesData}
                        metric="totalRevenue"
                        isLoading={isLoading}
                        customizable={true}
                      />
                      <CustomChart
                        type="bar"
                        title="Platform Performance Comparison"
                        data={analyticsData?.platformBreakdown}
                        metric="revenue"
                        isLoading={isLoading}
                        customizable={true}
                      />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                      <CustomChart
                        type="pie"
                        title="Revenue Distribution by Channel"
                        data={analyticsData?.d2cMetrics?.revenuePerChannel}
                        isLoading={isLoading}
                        customizable={true}
                      />
                      <CustomChart
                        type="gauge"
                        title="Return on Ad Spend (ROAS)"
                        data={analyticsData?.adMetrics?.returnOnAdSpend}
                        isLoading={isLoading}
                        customizable={true}
                      />
                      <CustomChart
                        type="area"
                        title="Customer Acquisition Growth"
                        data={analyticsData?.timeSeriesData}
                        metric="newCustomerCount"
                        isLoading={isLoading}
                        customizable={true}
                      />
                    </div>
                  </>
                )}
              </TabsContent>

              <TabsContent value="exhaustive" className="space-y-6">
                <ExhaustiveMetricsGrid 
                  data={analyticsData} 
                  isLoading={isLoading}
                  platforms={selectedPlatforms}
                  timeRange={timeRange}
                />
              </TabsContent>

              <TabsContent value="revenue" className="space-y-6">
                <PLReport 
                  data={analyticsData} 
                  platforms={selectedPlatforms}
                  timeRange={timeRange}
                />
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <CustomChart
                    type="line"
                    title="Revenue vs Costs Analysis"
                    data={analyticsData?.timeSeriesData}
                    metric="revenue"
                    isLoading={isLoading}
                    customizable={true}
                  />
                  <CustomChart
                    type="bar"
                    title="Profit Margin Trends"
                    data={analyticsData?.timeSeriesData}
                    metric="grossMargin"
                    isLoading={isLoading}
                    customizable={true}
                  />
                </div>
              </TabsContent>

              <TabsContent value="marketing" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <CustomChart
                    type="funnel"
                    title="Marketing Funnel Analysis"
                    data={analyticsData?.adMetrics}
                    isLoading={isLoading}
                    customizable={true}
                  />
                  <CustomChart
                    type="scatter"
                    title="Ad Spend vs Revenue Correlation"
                    data={analyticsData?.timeSeriesData}
                    isLoading={isLoading}
                    customizable={true}
                  />
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <CustomChart
                    type="gauge"
                    title="Click-Through Rate (CTR)"
                    data={analyticsData?.adMetrics?.clickThroughRate}
                    isLoading={isLoading}
                    customizable={true}
                  />
                  <CustomChart
                    type="gauge"
                    title="Conversion Rate"
                    data={analyticsData?.adMetrics?.conversionRate}
                    isLoading={isLoading}
                    customizable={true}
                  />
                  <CustomChart
                    type="gauge"
                    title="Cost Per Acquisition (CPA)"
                    data={analyticsData?.adMetrics?.costPerAction}
                    isLoading={isLoading}
                    customizable={true}
                  />
                </div>
              </TabsContent>

              <TabsContent value="operations" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <CustomChart
                    type="heatmap"
                    title="Delivery Performance Heatmap"
                    data={analyticsData?.deliveryMetrics}
                    isLoading={isLoading}
                    customizable={true}
                  />
                  <CustomChart
                    type="bar"
                    title="Inventory Turnover Analysis"
                    data={analyticsData?.d2cMetrics}
                    metric="inventoryTurnover"
                    isLoading={isLoading}
                    customizable={true}
                  />
                </div>
              </TabsContent>

              <TabsContent value="custom" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-1">
                    <ChartCustomizer onAddChart={handleAddCustomChart} />
                  </div>
                  <div className="lg:col-span-2">
                    <Card>
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <Plus className="h-5 w-5" />
                          Your Custom Charts
                        </CardTitle>
                        <CardDescription>
                          Create unlimited custom visualizations with any combination of metrics
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        {customCharts.length === 0 ? (
                          <div className="text-center py-8 text-muted-foreground">
                            <BarChart3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                            <p>No custom charts yet. Create your first chart using the customizer!</p>
                          </div>
                        ) : (
                          <div className="grid grid-cols-1 gap-4">
                            {customCharts.map((config, index) => (
                              <div key={index} className="border rounded-lg p-4">
                                <CustomChart
                                  type={config.type}
                                  title={`Custom Chart ${index + 1}`}
                                  data={analyticsData}
                                  metric={config.metric}
                                  isLoading={isLoading}
                                  customizable={true}
                                />
                              </div>
                            ))}
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </TabsContent>
            </Tabs>
          </div>

          {/* Enhanced AI Assistant Sidebar */}
          {showAI && (
            <div className="lg:col-span-1">
              <AIAssistant 
                data={analyticsData}
                onQuery={askAI}
                isProcessing={isProcessing}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}