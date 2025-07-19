"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Users, 
  ShoppingCart, 
  DollarSign, 
  Target,
  Package,
  Truck,
  Eye,
  MousePointer,
  RefreshCw,
  Download,
  Settings,
  AlertCircle,
  CheckCircle,
  Clock,
  ArrowUpRight,
  ArrowDownRight
} from "lucide-react"
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Sample data - replace with real API calls
const revenueData = [
  { month: 'Jan', revenue: 185000, orders: 1240, customers: 890 },
  { month: 'Feb', revenue: 220000, orders: 1450, customers: 1020 },
  { month: 'Mar', revenue: 195000, orders: 1320, customers: 950 },
  { month: 'Apr', revenue: 275000, orders: 1680, customers: 1180 },
  { month: 'May', revenue: 310000, orders: 1890, customers: 1350 },
  { month: 'Jun', revenue: 285000, orders: 1750, customers: 1220 },
]

const platformData = [
  { name: 'Shopify', revenue: 1250000, percentage: 45, color: '#8B5CF6' },
  { name: 'Amazon', revenue: 850000, percentage: 30, color: '#3B82F6' },
  { name: 'Facebook Ads', revenue: 420000, percentage: 15, color: '#10B981' },
  { name: 'Google Ads', revenue: 280000, percentage: 10, color: '#F59E0B' },
]

const adMetrics = [
  { platform: 'Facebook', spend: 125000, impressions: 2500000, clicks: 45000, conversions: 1800, roas: 4.2 },
  { platform: 'Google', spend: 98000, impressions: 1800000, clicks: 38000, conversions: 1520, roas: 3.8 },
  { platform: 'Instagram', spend: 75000, impressions: 1200000, clicks: 28000, conversions: 980, roas: 3.5 },
]

const deliveryMetrics = [
  { courier: 'Shiprocket', orders: 2500, onTime: 94.5, avgTime: 2.3, cost: 185000 },
  { courier: 'Delhivery', orders: 1800, onTime: 92.1, avgTime: 2.8, cost: 142000 },
  { courier: 'BlueDart', orders: 950, onTime: 96.2, avgTime: 1.9, cost: 98000 },
]

export default function DashboardPage() {
  const [selectedPlatforms, setSelectedPlatforms] = useState("all")
  const [timeRange, setTimeRange] = useState("30d")
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdated, setLastUpdated] = useState(new Date())

  const refreshData = async () => {
    setIsLoading(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    setLastUpdated(new Date())
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">D2C Analytics Dashboard</h1>
              <p className="text-gray-600 mt-1">
                Last updated: {lastUpdated.toLocaleString()}
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Select value={selectedPlatforms} onValueChange={setSelectedPlatforms}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Select platforms" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Platforms</SelectItem>
                  <SelectItem value="shopify">Shopify Only</SelectItem>
                  <SelectItem value="amazon">Amazon Only</SelectItem>
                  <SelectItem value="ads">Ads Only</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={timeRange} onValueChange={setTimeRange}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Time range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 90 days</SelectItem>
                  <SelectItem value="1y">Last year</SelectItem>
                </SelectContent>
              </Select>
              
              <Button onClick={refreshData} disabled={isLoading} variant="outline">
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              
              <Button>
                <Download className="h-4 w-4 mr-2" />
                Export P&L
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">₹2,78,50,000</div>
              <div className="flex items-center text-xs text-green-600">
                <ArrowUpRight className="h-3 w-3 mr-1" />
                +23.5% from last month
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Orders</CardTitle>
              <ShoppingCart className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">15,247</div>
              <div className="flex items-center text-xs text-green-600">
                <ArrowUpRight className="h-3 w-3 mr-1" />
                +18.2% from last month
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Average ROAS</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">4.2x</div>
              <div className="flex items-center text-xs text-green-600">
                <ArrowUpRight className="h-3 w-3 mr-1" />
                +0.3x from last month
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Customers</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">8,543</div>
              <div className="flex items-center text-xs text-green-600">
                <ArrowUpRight className="h-3 w-3 mr-1" />
                +12.1% from last month
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Platform Status */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Settings className="h-5 w-5 mr-2" />
              Platform Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[
                { name: 'Shopify', status: 'connected', lastSync: '2 min ago', records: '12,450' },
                { name: 'Facebook Ads', status: 'connected', lastSync: '5 min ago', records: '8,920' },
                { name: 'Google Ads', status: 'connected', lastSync: '3 min ago', records: '6,780' },
                { name: 'Shiprocket', status: 'syncing', lastSync: 'syncing...', records: '15,240' },
              ].map((platform) => (
                <div key={platform.name} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <div className="font-medium">{platform.name}</div>
                    <div className="text-sm text-gray-500">{platform.records} records</div>
                    <div className="text-xs text-gray-400">Last sync: {platform.lastSync}</div>
                  </div>
                  <div className="flex items-center">
                    {platform.status === 'connected' ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : platform.status === 'syncing' ? (
                      <Clock className="h-5 w-5 text-yellow-500 animate-pulse" />
                    ) : (
                      <AlertCircle className="h-5 w-5 text-red-500" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Main Analytics Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="revenue">Revenue</TabsTrigger>
            <TabsTrigger value="marketing">Marketing</TabsTrigger>
            <TabsTrigger value="operations">Operations</TabsTrigger>
            <TabsTrigger value="customers">Customers</TabsTrigger>
            <TabsTrigger value="pl">P&L Report</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Revenue Trend */}
              <Card>
                <CardHeader>
                  <CardTitle>Revenue Trend</CardTitle>
                  <CardDescription>Monthly revenue over the last 6 months</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={revenueData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`₹${value.toLocaleString()}`, 'Revenue']} />
                      <Area type="monotone" dataKey="revenue" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
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
                        label={({ name, percentage }) => `${name} ${percentage}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="revenue"
                      >
                        {platformData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`₹${value.toLocaleString()}`, 'Revenue']} />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Orders and Customers */}
            <Card>
              <CardHeader>
                <CardTitle>Orders & Customer Growth</CardTitle>
                <CardDescription>Monthly orders and new customers</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={revenueData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="orders" fill="#3B82F6" name="Orders" />
                    <Bar dataKey="customers" fill="#10B981" name="New Customers" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Marketing Tab */}
          <TabsContent value="marketing" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Total Ad Spend</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">₹2,98,000</div>
                  <div className="text-xs text-red-600 flex items-center">
                    <ArrowUpRight className="h-3 w-3 mr-1" />
                    +15.2% from last month
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Total Conversions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">4,300</div>
                  <div className="text-xs text-green-600 flex items-center">
                    <ArrowUpRight className="h-3 w-3 mr-1" />
                    +8.7% from last month
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Average CPC</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">₹12.50</div>
                  <div className="text-xs text-green-600 flex items-center">
                    <ArrowDownRight className="h-3 w-3 mr-1" />
                    -5.3% from last month
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Ad Performance Table */}
            <Card>
              <CardHeader>
                <CardTitle>Ad Platform Performance</CardTitle>
                <CardDescription>Detailed performance metrics by platform</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left p-2">Platform</th>
                        <th className="text-right p-2">Spend</th>
                        <th className="text-right p-2">Impressions</th>
                        <th className="text-right p-2">Clicks</th>
                        <th className="text-right p-2">Conversions</th>
                        <th className="text-right p-2">ROAS</th>
                      </tr>
                    </thead>
                    <tbody>
                      {adMetrics.map((metric) => (
                        <tr key={metric.platform} className="border-b">
                          <td className="p-2 font-medium">{metric.platform}</td>
                          <td className="p-2 text-right">₹{metric.spend.toLocaleString()}</td>
                          <td className="p-2 text-right">{metric.impressions.toLocaleString()}</td>
                          <td className="p-2 text-right">{metric.clicks.toLocaleString()}</td>
                          <td className="p-2 text-right">{metric.conversions.toLocaleString()}</td>
                          <td className="p-2 text-right">
                            <Badge variant={metric.roas >= 4 ? "default" : metric.roas >= 3 ? "secondary" : "destructive"}>
                              {metric.roas}x
                            </Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Operations Tab */}
          <TabsContent value="operations" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Total Shipments</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">5,250</div>
                  <div className="text-xs text-green-600">+12% this month</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">On-time Delivery</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">94.2%</div>
                  <div className="text-xs text-green-600">+2.1% improvement</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Avg Delivery Time</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">2.3 days</div>
                  <div className="text-xs text-green-600">-0.2 days faster</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Return Rate</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">2.1%</div>
                  <div className="text-xs text-red-600">+0.3% increase</div>
                </CardContent>
              </Card>
            </div>

            {/* Delivery Performance */}
            <Card>
              <CardHeader>
                <CardTitle>Delivery Partner Performance</CardTitle>
                <CardDescription>Performance metrics by courier partner</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left p-2">Courier</th>
                        <th className="text-right p-2">Orders</th>
                        <th className="text-right p-2">On-time %</th>
                        <th className="text-right p-2">Avg Time</th>
                        <th className="text-right p-2">Total Cost</th>
                      </tr>
                    </thead>
                    <tbody>
                      {deliveryMetrics.map((metric) => (
                        <tr key={metric.courier} className="border-b">
                          <td className="p-2 font-medium">{metric.courier}</td>
                          <td className="p-2 text-right">{metric.orders.toLocaleString()}</td>
                          <td className="p-2 text-right">
                            <Badge variant={metric.onTime >= 95 ? "default" : metric.onTime >= 90 ? "secondary" : "destructive"}>
                              {metric.onTime}%
                            </Badge>
                          </td>
                          <td className="p-2 text-right">{metric.avgTime} days</td>
                          <td className="p-2 text-right">₹{metric.cost.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* P&L Report Tab */}
          <TabsContent value="pl" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Profit & Loss Statement</CardTitle>
                <CardDescription>Comprehensive P&L for selected platforms and time period</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-8">
                    <div>
                      <h3 className="font-semibold text-lg mb-4 text-green-600">Revenue</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Shopify Sales</span>
                          <span>₹12,50,000</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Amazon Sales</span>
                          <span>₹8,50,000</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Other Platforms</span>
                          <span>₹4,20,000</span>
                        </div>
                        <div className="flex justify-between font-bold border-t pt-2">
                          <span>Total Revenue</span>
                          <span>₹25,20,000</span>
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <h3 className="font-semibold text-lg mb-4 text-red-600">Costs</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Cost of Goods Sold</span>
                          <span>₹10,08,000</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Ad Spend</span>
                          <span>₹2,98,000</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Shipping Costs</span>
                          <span>₹1,85,000</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Platform Fees</span>
                          <span>₹1,26,000</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Other Expenses</span>
                          <span>₹95,000</span>
                        </div>
                        <div className="flex justify-between font-bold border-t pt-2">
                          <span>Total Costs</span>
                          <span>₹17,12,000</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="border-t pt-4">
                    <div className="grid grid-cols-3 gap-8 text-center">
                      <div>
                        <div className="text-2xl font-bold text-green-600">₹8,08,000</div>
                        <div className="text-sm text-gray-600">Gross Profit</div>
                        <div className="text-xs text-gray-500">32.1% margin</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-blue-600">₹7,13,000</div>
                        <div className="text-sm text-gray-600">Operating Profit</div>
                        <div className="text-xs text-gray-500">28.3% margin</div>
                      </div>
                      <div>
                        <div className="text-2xl font-bold text-purple-600">₹6,85,000</div>
                        <div className="text-sm text-gray-600">Net Profit</div>
                        <div className="text-xs text-gray-500">27.2% margin</div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}