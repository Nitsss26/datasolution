'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  ComposedChart,
  Scatter,
  ScatterChart,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Treemap,
  FunnelChart,
  Funnel,
  LabelList
} from 'recharts'
import { 
  TrendingUp, 
  BarChart3, 
  PieChart as PieChartIcon, 
  Activity,
  Target,
  DollarSign,
  Users,
  ShoppingCart,
  Truck,
  Eye,
  MousePointer,
  Download,
  Settings,
  Maximize2
} from 'lucide-react'

// Sample data for different chart types
const revenueData = [
  { month: 'Jan', shopify: 1250000, amazon: 850000, direct: 420000, ads_spend: 298000 },
  { month: 'Feb', shopify: 1420000, amazon: 920000, direct: 480000, ads_spend: 325000 },
  { month: 'Mar', shopify: 1180000, amazon: 780000, direct: 390000, ads_spend: 285000 },
  { month: 'Apr', shopify: 1680000, amazon: 1120000, direct: 560000, ads_spend: 398000 },
  { month: 'May', shopify: 1890000, amazon: 1280000, direct: 640000, ads_spend: 445000 },
  { month: 'Jun', shopify: 1750000, amazon: 1180000, direct: 590000, ads_spend: 412000 },
]

const platformDistribution = [
  { name: 'Shopify', value: 45, revenue: 12500000, color: '#8B5CF6' },
  { name: 'Amazon', value: 30, revenue: 8500000, color: '#3B82F6' },
  { name: 'Direct Sales', value: 15, revenue: 4200000, color: '#10B981' },
  { name: 'Marketplaces', value: 10, revenue: 2800000, color: '#F59E0B' },
]

const customerSegments = [
  { segment: 'High Value', customers: 1250, revenue: 8500000, avg_order: 6800 },
  { segment: 'Regular', customers: 4580, revenue: 12400000, avg_order: 2700 },
  { segment: 'New', customers: 2890, revenue: 4200000, avg_order: 1450 },
  { segment: 'Churned', customers: 890, revenue: 980000, avg_order: 1100 },
]

const adPerformanceData = [
  { platform: 'Google Ads', spend: 125000, revenue: 525000, roas: 4.2, impressions: 2500000, clicks: 45000 },
  { platform: 'Facebook Ads', spend: 98000, revenue: 372400, roas: 3.8, impressions: 1800000, clicks: 38000 },
  { platform: 'Instagram Ads', spend: 75000, revenue: 262500, roas: 3.5, impressions: 1200000, clicks: 28000 },
  { platform: 'YouTube Ads', spend: 45000, revenue: 135000, roas: 3.0, impressions: 800000, clicks: 15000 },
]

const deliveryPerformance = [
  { courier: 'Shiprocket', orders: 2500, onTime: 94.5, avgTime: 2.3, cost: 185000 },
  { courier: 'Delhivery', orders: 1800, onTime: 92.1, avgTime: 2.8, cost: 142000 },
  { courier: 'BlueDart', orders: 950, onTime: 96.2, avgTime: 1.9, cost: 98000 },
  { courier: 'DTDC', orders: 720, onTime: 89.5, avgTime: 3.2, cost: 78000 },
]

const conversionFunnel = [
  { stage: 'Visitors', value: 125000, percentage: 100 },
  { stage: 'Product Views', value: 45000, percentage: 36 },
  { stage: 'Add to Cart', value: 18000, percentage: 14.4 },
  { stage: 'Checkout', value: 12000, percentage: 9.6 },
  { stage: 'Purchase', value: 8500, percentage: 6.8 },
]

const productPerformance = [
  { name: 'Premium T-Shirts', revenue: 2850000, units: 12450, margin: 65 },
  { name: 'Wireless Headphones', revenue: 1920000, units: 3840, margin: 45 },
  { name: 'Smart Watches', revenue: 1680000, units: 2100, margin: 55 },
  { name: 'Phone Cases', revenue: 890000, units: 8900, margin: 70 },
  { name: 'Bluetooth Speakers', revenue: 750000, units: 1500, margin: 40 },
]

const geographicData = [
  { state: 'Maharashtra', orders: 4580, revenue: 3250000 },
  { state: 'Delhi', orders: 3920, revenue: 2890000 },
  { state: 'Karnataka', orders: 3450, revenue: 2650000 },
  { state: 'Tamil Nadu', orders: 2890, revenue: 2180000 },
  { state: 'Gujarat', orders: 2340, revenue: 1890000 },
  { state: 'West Bengal', orders: 1980, revenue: 1450000 },
]

const cohortData = [
  { month: 'Jan', week1: 100, week2: 85, week3: 72, week4: 65 },
  { month: 'Feb', week1: 100, week2: 88, week3: 75, week4: 68 },
  { month: 'Mar', week1: 100, week2: 82, week3: 69, week4: 62 },
  { month: 'Apr', week1: 100, week2: 90, week3: 78, week4: 71 },
  { month: 'May', week1: 100, week2: 87, week3: 74, week4: 67 },
  { month: 'Jun', week1: 100, week2: 85, week3: 72, week4: 65 },
]

export function ComprehensiveCharts() {
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d')
  const [selectedMetric, setSelectedMetric] = useState('revenue')
  const [chartType, setChartType] = useState('line')

  const COLORS = ['#8B5CF6', '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5A2B']

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
          <p className="text-gray-600">Comprehensive data visualization and insights</p>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={selectedTimeRange} onValueChange={setSelectedTimeRange}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
              <SelectItem value="1y">Last year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button variant="outline">
            <Settings className="h-4 w-4 mr-2" />
            Customize
          </Button>
        </div>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="revenue">Revenue</TabsTrigger>
          <TabsTrigger value="marketing">Marketing</TabsTrigger>
          <TabsTrigger value="customers">Customers</TabsTrigger>
          <TabsTrigger value="operations">Operations</TabsTrigger>
          <TabsTrigger value="advanced">Advanced</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Revenue Trend */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <TrendingUp className="h-5 w-5 mr-2" />
                    Revenue Trend
                  </div>
                  <Button variant="ghost" size="sm">
                    <Maximize2 className="h-4 w-4" />
                  </Button>
                </CardTitle>
                <CardDescription>Monthly revenue across all platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <ComposedChart data={revenueData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`₹${value.toLocaleString()}`, '']} />
                    <Legend />
                    <Area type="monotone" dataKey="shopify" stackId="1" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.6} name="Shopify" />
                    <Area type="monotone" dataKey="amazon" stackId="1" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.6} name="Amazon" />
                    <Area type="monotone" dataKey="direct" stackId="1" stroke="#10B981" fill="#10B981" fillOpacity={0.6} name="Direct" />
                    <Line type="monotone" dataKey="ads_spend" stroke="#EF4444" strokeWidth={3} name="Ad Spend" />
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Platform Distribution */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <PieChartIcon className="h-5 w-5 mr-2" />
                    Revenue by Platform
                  </div>
                  <Button variant="ghost" size="sm">
                    <Maximize2 className="h-4 w-4" />
                  </Button>
                </CardTitle>
                <CardDescription>Revenue distribution across platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={platformDistribution}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {platformDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [`${value}%`, 'Share']} />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Key Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                    <p className="text-2xl font-bold">₹2.85M</p>
                    <p className="text-xs text-green-600">+23.5% vs last month</p>
                  </div>
                  <DollarSign className="h-8 w-8 text-green-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Orders</p>
                    <p className="text-2xl font-bold">15,247</p>
                    <p className="text-xs text-green-600">+18.2% vs last month</p>
                  </div>
                  <ShoppingCart className="h-8 w-8 text-blue-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Average ROAS</p>
                    <p className="text-2xl font-bold">4.2x</p>
                    <p className="text-xs text-green-600">+0.3x vs last month</p>
                  </div>
                  <Target className="h-8 w-8 text-purple-600" />
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Active Customers</p>
                    <p className="text-2xl font-bold">8,543</p>
                    <p className="text-xs text-green-600">+12.1% vs last month</p>
                  </div>
                  <Users className="h-8 w-8 text-orange-600" />
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Revenue Tab */}
        <TabsContent value="revenue" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Product Performance */}
            <Card>
              <CardHeader>
                <CardTitle>Top Products by Revenue</CardTitle>
                <CardDescription>Best performing products this month</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={productPerformance} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="name" type="category" width={120} />
                    <Tooltip formatter={(value) => [`₹${value.toLocaleString()}`, 'Revenue']} />
                    <Bar dataKey="revenue" fill="#8B5CF6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Geographic Revenue */}
            <Card>
              <CardHeader>
                <CardTitle>Revenue by State</CardTitle>
                <CardDescription>Geographic distribution of sales</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={geographicData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="state" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`₹${value.toLocaleString()}`, 'Revenue']} />
                    <Bar dataKey="revenue" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Revenue vs Profit Margin */}
          <Card>
            <CardHeader>
              <CardTitle>Revenue vs Profit Margin Analysis</CardTitle>
              <CardDescription>Product performance matrix</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <ScatterChart data={productPerformance}>
                  <CartesianGrid />
                  <XAxis dataKey="revenue" name="Revenue" />
                  <YAxis dataKey="margin" name="Margin %" />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Scatter name="Products" dataKey="margin" fill="#8B5CF6" />
                </ScatterChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Marketing Tab */}
        <TabsContent value="marketing" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Ad Performance Comparison */}
            <Card>
              <CardHeader>
                <CardTitle>Ad Platform Performance</CardTitle>
                <CardDescription>ROAS and spend comparison</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <ComposedChart data={adPerformanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Legend />
                    <Bar yAxisId="left" dataKey="spend" fill="#EF4444" name="Spend (₹)" />
                    <Line yAxisId="right" type="monotone" dataKey="roas" stroke="#10B981" strokeWidth={3} name="ROAS" />
                  </ComposedChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Conversion Funnel */}
            <Card>
              <CardHeader>
                <CardTitle>Conversion Funnel</CardTitle>
                <CardDescription>Customer journey analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <FunnelChart>
                    <Tooltip />
                    <Funnel
                      dataKey="value"
                      data={conversionFunnel}
                      isAnimationActive
                    >
                      <LabelList position="center" fill="#fff" stroke="none" />
                    </Funnel>
                  </FunnelChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Marketing ROI Radar */}
          <Card>
            <CardHeader>
              <CardTitle>Marketing Performance Radar</CardTitle>
              <CardDescription>Multi-dimensional performance analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={adPerformanceData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="platform" />
                  <PolarRadiusAxis angle={90} domain={[0, 5]} />
                  <Radar name="ROAS" dataKey="roas" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.3} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Customers Tab */}
        <TabsContent value="customers" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Customer Segments */}
            <Card>
              <CardHeader>
                <CardTitle>Customer Segmentation</CardTitle>
                <CardDescription>Revenue by customer segments</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={customerSegments}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="segment" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`₹${value.toLocaleString()}`, 'Revenue']} />
                    <Bar dataKey="revenue" fill="#10B981" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Customer Retention Cohort */}
            <Card>
              <CardHeader>
                <CardTitle>Customer Retention Cohort</CardTitle>
                <CardDescription>Monthly retention rates</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={cohortData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="week1" stroke="#8B5CF6" name="Week 1" />
                    <Line type="monotone" dataKey="week2" stroke="#3B82F6" name="Week 2" />
                    <Line type="monotone" dataKey="week3" stroke="#10B981" name="Week 3" />
                    <Line type="monotone" dataKey="week4" stroke="#F59E0B" name="Week 4" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Customer Lifetime Value */}
          <Card>
            <CardHeader>
              <CardTitle>Customer Lifetime Value Distribution</CardTitle>
              <CardDescription>CLV across different customer segments</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <Treemap
                  data={customerSegments}
                  dataKey="revenue"
                  ratio={4/3}
                  stroke="#fff"
                  fill="#8B5CF6"
                />
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Operations Tab */}
        <TabsContent value="operations" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Delivery Performance */}
            <Card>
              <CardHeader>
                <CardTitle>Delivery Performance</CardTitle>
                <CardDescription>On-time delivery rates by courier</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={deliveryPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="courier" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="onTime" fill="#10B981" name="On-time %" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Shipping Cost vs Volume */}
            <Card>
              <CardHeader>
                <CardTitle>Shipping Cost Analysis</CardTitle>
                <CardDescription>Cost efficiency by courier partner</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <ScatterChart data={deliveryPerformance}>
                    <CartesianGrid />
                    <XAxis dataKey="orders" name="Orders" />
                    <YAxis dataKey="cost" name="Cost" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Couriers" dataKey="cost" fill="#3B82F6" />
                  </ScatterChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Advanced Tab */}
        <TabsContent value="advanced" className="space-y-6">
          <div className="grid grid-cols-1 gap-6">
            {/* Custom Chart Builder */}
            <Card>
              <CardHeader>
                <CardTitle>Custom Chart Builder</CardTitle>
                <CardDescription>Create your own visualizations</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <Select value={chartType} onValueChange={setChartType}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chart Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="line">Line Chart</SelectItem>
                      <SelectItem value="bar">Bar Chart</SelectItem>
                      <SelectItem value="area">Area Chart</SelectItem>
                      <SelectItem value="pie">Pie Chart</SelectItem>
                      <SelectItem value="scatter">Scatter Plot</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Select value={selectedMetric} onValueChange={setSelectedMetric}>
                    <SelectTrigger>
                      <SelectValue placeholder="Metric" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="revenue">Revenue</SelectItem>
                      <SelectItem value="orders">Orders</SelectItem>
                      <SelectItem value="customers">Customers</SelectItem>
                      <SelectItem value="roas">ROAS</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Button>
                    <BarChart3 className="h-4 w-4 mr-2" />
                    Generate Chart
                  </Button>
                </div>
                
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                  <BarChart3 className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-500">Your custom chart will appear here</p>
                  <p className="text-sm text-gray-400">Select chart type and metrics to get started</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}