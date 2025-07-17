"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts"
import { TrendingUp, TrendingDown, DollarSign, ShoppingCart, Target, Download, RefreshCw } from "lucide-react"

// Mock data for demonstration
const mockMetrics = {
  totalRevenue: { value: 245000, change: 12.5 },
  totalOrders: { value: 1250, change: 8.3 },
  averageOrderValue: { value: 196, change: -2.1 },
  roas: { value: 4.2, change: 15.7 },
}

const revenueData = [
  { date: "2024-01-01", revenue: 12000, orders: 65 },
  { date: "2024-01-02", revenue: 15000, orders: 78 },
  { date: "2024-01-03", revenue: 18000, orders: 92 },
  { date: "2024-01-04", revenue: 14000, orders: 71 },
  { date: "2024-01-05", revenue: 22000, orders: 115 },
  { date: "2024-01-06", revenue: 19000, orders: 98 },
  { date: "2024-01-07", revenue: 25000, orders: 128 },
]

const platformData = [
  { name: "Shopify", revenue: 120000, color: "#8884d8" },
  { name: "Amazon", revenue: 85000, color: "#82ca9d" },
  { name: "Facebook Ads", revenue: 25000, color: "#ffc658" },
  { name: "Google Ads", revenue: 15000, color: "#ff7300" },
]

const adPerformanceData = [
  { platform: "Facebook", spend: 15000, revenue: 63000, roas: 4.2 },
  { platform: "Google", spend: 12000, revenue: 48000, roas: 4.0 },
  { platform: "Instagram", spend: 8000, revenue: 28000, roas: 3.5 },
]

export default function DashboardPage() {
  const [timeRange, setTimeRange] = useState("30d")
  const [selectedPlatforms, setSelectedPlatforms] = useState("all")
  const [isLoading, setIsLoading] = useState(false)

  const handleRefresh = async () => {
    setIsLoading(true)
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-gray-600">Welcome back! Here's your business overview.</p>
            </div>
            <div className="flex items-center space-x-4">
              <Select value={timeRange} onValueChange={setTimeRange}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="15d">Last 15 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 90 days</SelectItem>
                </SelectContent>
              </Select>
              <Button onClick={handleRefresh} disabled={isLoading}>
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`} />
                Refresh
              </Button>
              <Button>
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium opacity-90">Total Revenue</CardTitle>
              <DollarSign className="h-4 w-4 opacity-90" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">₹{mockMetrics.totalRevenue.value.toLocaleString()}</div>
              <div className="flex items-center text-xs opacity-90">
                <TrendingUp className="h-3 w-3 mr-1" />+{mockMetrics.totalRevenue.change}% from last period
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium opacity-90">Total Orders</CardTitle>
              <ShoppingCart className="h-4 w-4 opacity-90" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{mockMetrics.totalOrders.value.toLocaleString()}</div>
              <div className="flex items-center text-xs opacity-90">
                <TrendingUp className="h-3 w-3 mr-1" />+{mockMetrics.totalOrders.change}% from last period
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium opacity-90">Average Order Value</CardTitle>
              <Target className="h-4 w-4 opacity-90" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">₹{mockMetrics.averageOrderValue.value}</div>
              <div className="flex items-center text-xs opacity-90">
                <TrendingDown className="h-3 w-3 mr-1" />
                {mockMetrics.averageOrderValue.change}% from last period
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-orange-500 to-orange-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium opacity-90">ROAS</CardTitle>
              <TrendingUp className="h-4 w-4 opacity-90" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{mockMetrics.roas.value}x</div>
              <div className="flex items-center text-xs opacity-90">
                <TrendingUp className="h-3 w-3 mr-1" />+{mockMetrics.roas.change}% from last period
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Revenue Trend Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Revenue Trend</CardTitle>
              <CardDescription>Daily revenue and order trends</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={revenueData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="revenue"
                    stackId="1"
                    stroke="#8884d8"
                    fill="#8884d8"
                    fillOpacity={0.6}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Platform Revenue Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>Revenue by Platform</CardTitle>
              <CardDescription>Revenue distribution across platforms</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={platformData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="revenue"
                  >
                    {platformData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Analytics Tabs */}
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="advertising">Advertising</TabsTrigger>
            <TabsTrigger value="platforms">Platforms</TabsTrigger>
            <TabsTrigger value="customers">Customers</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Orders vs Revenue</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={revenueData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis yAxisId="left" />
                      <YAxis yAxisId="right" orientation="right" />
                      <Tooltip />
                      <Legend />
                      <Bar yAxisId="left" dataKey="orders" fill="#8884d8" />
                      <Line yAxisId="right" type="monotone" dataKey="revenue" stroke="#82ca9d" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Top Performing Products</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { name: "Premium T-Shirt", revenue: 45000, orders: 230 },
                      { name: "Wireless Headphones", revenue: 38000, orders: 152 },
                      { name: "Smart Watch", revenue: 32000, orders: 89 },
                      { name: "Running Shoes", revenue: 28000, orders: 140 },
                    ].map((product, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">{product.name}</p>
                          <p className="text-sm text-gray-600">{product.orders} orders</p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold">₹{product.revenue.toLocaleString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="advertising" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Ad Performance by Platform</CardTitle>
                <CardDescription>Compare advertising performance across platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={adPerformanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="spend" fill="#8884d8" name="Ad Spend" />
                    <Bar dataKey="revenue" fill="#82ca9d" name="Revenue" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {adPerformanceData.map((platform, index) => (
                <Card key={index}>
                  <CardHeader>
                    <CardTitle className="text-lg">{platform.platform}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Spend:</span>
                        <span className="font-medium">₹{platform.spend.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Revenue:</span>
                        <span className="font-medium">₹{platform.revenue.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">ROAS:</span>
                        <Badge variant={platform.roas >= 4 ? "default" : "secondary"}>{platform.roas}x</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="platforms" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {platformData.map((platform, index) => (
                <Card key={index}>
                  <CardHeader>
                    <CardTitle className="text-lg">{platform.name}</CardTitle>
                    <Badge variant="outline">Connected</Badge>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold mb-2">₹{platform.revenue.toLocaleString()}</div>
                    <p className="text-sm text-gray-600">Total Revenue</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="customers" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Customer Acquisition</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span>New Customers</span>
                      <span className="font-bold">1,234</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Returning Customers</span>
                      <span className="font-bold">856</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Customer Retention Rate</span>
                      <Badge>68.5%</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Customer Lifetime Value</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold mb-2">₹2,450</div>
                  <p className="text-sm text-gray-600 mb-4">Average CLV</p>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Average Order Value</span>
                      <span className="text-sm font-medium">₹196</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Purchase Frequency</span>
                      <span className="text-sm font-medium">2.3x/year</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
