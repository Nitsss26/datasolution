'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { 
  ShoppingBag, 
  Target, 
  Truck, 
  Users,
  DollarSign,
  TrendingUp,
  TrendingDown,
  Search,
  Filter,
  Download,
  RefreshCw,
  Eye,
  ArrowUpDown,
  MoreHorizontal
} from 'lucide-react'

// Sample data for different platforms
const shopifyData = [
  {
    id: 'SH001',
    date: '2024-01-15',
    order_id: 'ORD-2024-001',
    customer_name: 'John Doe',
    product_name: 'Premium T-Shirt',
    quantity: 2,
    unit_price: 1299,
    total_amount: 2598,
    discount: 260,
    tax: 467,
    shipping: 99,
    payment_method: 'Credit Card',
    status: 'Delivered',
    channel: 'Online Store',
    location: 'Mumbai, MH'
  },
  {
    id: 'SH002',
    date: '2024-01-15',
    order_id: 'ORD-2024-002',
    customer_name: 'Jane Smith',
    product_name: 'Wireless Headphones',
    quantity: 1,
    unit_price: 4999,
    total_amount: 4999,
    discount: 500,
    tax: 810,
    shipping: 0,
    payment_method: 'UPI',
    status: 'Processing',
    channel: 'Mobile App',
    location: 'Delhi, DL'
  },
  // Add more sample data...
]

const googleAdsData = [
  {
    id: 'GA001',
    date: '2024-01-15',
    campaign_name: 'Summer Sale 2024',
    ad_group: 'T-Shirts',
    keyword: 'premium t-shirt',
    impressions: 12450,
    clicks: 234,
    ctr: 1.88,
    cpc: 12.50,
    cost: 2925,
    conversions: 18,
    conversion_rate: 7.69,
    cpa: 162.50,
    roas: 4.2,
    quality_score: 8
  },
  {
    id: 'GA002',
    date: '2024-01-15',
    campaign_name: 'Brand Awareness',
    ad_group: 'Electronics',
    keyword: 'wireless headphones',
    impressions: 8920,
    clicks: 156,
    ctr: 1.75,
    cpc: 18.75,
    cost: 2925,
    conversions: 12,
    conversion_rate: 7.69,
    cpa: 243.75,
    roas: 3.8,
    quality_score: 7
  },
  // Add more sample data...
]

const metaAdsData = [
  {
    id: 'MA001',
    date: '2024-01-15',
    campaign_name: 'Retargeting Campaign',
    ad_set: 'Lookalike Audience',
    ad_name: 'Video Ad - Product Demo',
    platform: 'Facebook',
    placement: 'News Feed',
    impressions: 15680,
    reach: 12340,
    clicks: 287,
    ctr: 1.83,
    cpc: 15.20,
    cost: 4362,
    conversions: 23,
    conversion_rate: 8.01,
    cpa: 189.65,
    roas: 4.5,
    engagement_rate: 3.2
  },
  {
    id: 'MA002',
    date: '2024-01-15',
    campaign_name: 'Brand Awareness',
    ad_set: 'Interest Targeting',
    ad_name: 'Carousel Ad - Products',
    platform: 'Instagram',
    placement: 'Stories',
    impressions: 9840,
    reach: 8120,
    clicks: 198,
    ctr: 2.01,
    cpc: 18.90,
    cost: 3742,
    conversions: 15,
    conversion_rate: 7.58,
    cpa: 249.47,
    roas: 3.9,
    engagement_rate: 4.1
  },
  // Add more sample data...
]

const shiprocketData = [
  {
    id: 'SR001',
    date: '2024-01-15',
    order_id: 'ORD-2024-001',
    awb: 'AWB123456789',
    courier: 'Delhivery',
    pickup_date: '2024-01-15',
    delivery_date: '2024-01-17',
    origin: 'Mumbai, MH',
    destination: 'Delhi, DL',
    weight: 0.5,
    dimensions: '20x15x5',
    shipping_cost: 89,
    cod_amount: 2598,
    status: 'Delivered',
    delivery_time: 2,
    attempts: 1,
    rto: false
  },
  {
    id: 'SR002',
    date: '2024-01-15',
    order_id: 'ORD-2024-002',
    awb: 'AWB987654321',
    courier: 'BlueDart',
    pickup_date: '2024-01-15',
    delivery_date: null,
    origin: 'Bangalore, KA',
    destination: 'Chennai, TN',
    weight: 1.2,
    dimensions: '25x20x10',
    shipping_cost: 125,
    cod_amount: 0,
    status: 'In Transit',
    delivery_time: null,
    attempts: 0,
    rto: false
  },
  // Add more sample data...
]

export function ComprehensiveDataTables() {
  const [activeTab, setActiveTab] = useState('shopify')
  const [searchTerm, setSearchTerm] = useState('')
  const [sortField, setSortField] = useState('')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')
  const [filterStatus, setFilterStatus] = useState('all')

  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const exportData = (format: string) => {
    // Implementation for data export
    console.log(`Exporting data in ${format} format`)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Comprehensive Data Tables</h2>
          <p className="text-gray-600">Detailed view of all your platform data</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={() => exportData('csv')}>
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
          <Button variant="outline" onClick={() => exportData('excel')}>
            <Download className="h-4 w-4 mr-2" />
            Export Excel
          </Button>
          <Button>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh Data
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex-1 min-w-[200px]">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search across all data..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Data Tables */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="shopify" className="flex items-center">
            <ShoppingBag className="h-4 w-4 mr-2" />
            Shopify Data
          </TabsTrigger>
          <TabsTrigger value="google-ads" className="flex items-center">
            <Target className="h-4 w-4 mr-2" />
            Google Ads
          </TabsTrigger>
          <TabsTrigger value="meta-ads" className="flex items-center">
            <Target className="h-4 w-4 mr-2" />
            Meta Ads
          </TabsTrigger>
          <TabsTrigger value="shiprocket" className="flex items-center">
            <Truck className="h-4 w-4 mr-2" />
            Shiprocket
          </TabsTrigger>
        </TabsList>

        {/* Shopify Data Tab */}
        <TabsContent value="shopify">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center">
                  <ShoppingBag className="h-5 w-5 mr-2" />
                  Shopify Orders & Sales Data
                </div>
                <Badge variant="outline">{shopifyData.length} records</Badge>
              </CardTitle>
              <CardDescription>
                Complete order details including customer info, products, payments, and fulfillment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="cursor-pointer" onClick={() => handleSort('date')}>
                        Date <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead>Order ID</TableHead>
                      <TableHead>Customer</TableHead>
                      <TableHead>Product</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('quantity')}>
                        Qty <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('total_amount')}>
                        Amount <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">Discount</TableHead>
                      <TableHead className="text-right">Tax</TableHead>
                      <TableHead className="text-right">Shipping</TableHead>
                      <TableHead>Payment</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Channel</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {shopifyData.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell className="font-medium">{row.date}</TableCell>
                        <TableCell className="font-mono text-sm">{row.order_id}</TableCell>
                        <TableCell>{row.customer_name}</TableCell>
                        <TableCell>{row.product_name}</TableCell>
                        <TableCell className="text-right">{row.quantity}</TableCell>
                        <TableCell className="text-right font-medium">₹{row.total_amount.toLocaleString()}</TableCell>
                        <TableCell className="text-right text-green-600">-₹{row.discount}</TableCell>
                        <TableCell className="text-right">₹{row.tax}</TableCell>
                        <TableCell className="text-right">₹{row.shipping}</TableCell>
                        <TableCell>{row.payment_method}</TableCell>
                        <TableCell>
                          <Badge variant={row.status === 'Delivered' ? 'default' : row.status === 'Processing' ? 'secondary' : 'destructive'}>
                            {row.status}
                          </Badge>
                        </TableCell>
                        <TableCell>{row.channel}</TableCell>
                        <TableCell>{row.location}</TableCell>
                        <TableCell>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Google Ads Data Tab */}
        <TabsContent value="google-ads">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center">
                  <Target className="h-5 w-5 mr-2" />
                  Google Ads Performance Data
                </div>
                <Badge variant="outline">{googleAdsData.length} records</Badge>
              </CardTitle>
              <CardDescription>
                Detailed campaign, ad group, and keyword performance metrics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Campaign</TableHead>
                      <TableHead>Ad Group</TableHead>
                      <TableHead>Keyword</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('impressions')}>
                        Impressions <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('clicks')}>
                        Clicks <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">CTR %</TableHead>
                      <TableHead className="text-right">CPC</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('cost')}>
                        Cost <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">Conv.</TableHead>
                      <TableHead className="text-right">Conv. Rate</TableHead>
                      <TableHead className="text-right">CPA</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('roas')}>
                        ROAS <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">QS</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {googleAdsData.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell className="font-medium">{row.date}</TableCell>
                        <TableCell className="max-w-[150px] truncate">{row.campaign_name}</TableCell>
                        <TableCell>{row.ad_group}</TableCell>
                        <TableCell className="font-mono text-sm">{row.keyword}</TableCell>
                        <TableCell className="text-right">{row.impressions.toLocaleString()}</TableCell>
                        <TableCell className="text-right">{row.clicks}</TableCell>
                        <TableCell className="text-right">{row.ctr}%</TableCell>
                        <TableCell className="text-right">₹{row.cpc}</TableCell>
                        <TableCell className="text-right font-medium">₹{row.cost.toLocaleString()}</TableCell>
                        <TableCell className="text-right">{row.conversions}</TableCell>
                        <TableCell className="text-right">{row.conversion_rate}%</TableCell>
                        <TableCell className="text-right">₹{row.cpa}</TableCell>
                        <TableCell className="text-right">
                          <Badge variant={row.roas >= 4 ? 'default' : row.roas >= 3 ? 'secondary' : 'destructive'}>
                            {row.roas}x
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right">
                          <Badge variant={row.quality_score >= 8 ? 'default' : row.quality_score >= 6 ? 'secondary' : 'destructive'}>
                            {row.quality_score}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Meta Ads Data Tab */}
        <TabsContent value="meta-ads">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center">
                  <Target className="h-5 w-5 mr-2" />
                  Meta Ads Performance Data
                </div>
                <Badge variant="outline">{metaAdsData.length} records</Badge>
              </CardTitle>
              <CardDescription>
                Facebook and Instagram ads performance across campaigns, ad sets, and individual ads
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Campaign</TableHead>
                      <TableHead>Ad Set</TableHead>
                      <TableHead>Ad Name</TableHead>
                      <TableHead>Platform</TableHead>
                      <TableHead>Placement</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('impressions')}>
                        Impressions <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">Reach</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('clicks')}>
                        Clicks <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">CTR %</TableHead>
                      <TableHead className="text-right">CPC</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('cost')}>
                        Cost <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">Conv.</TableHead>
                      <TableHead className="text-right">Conv. Rate</TableHead>
                      <TableHead className="text-right">CPA</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('roas')}>
                        ROAS <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">Eng. Rate</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {metaAdsData.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell className="font-medium">{row.date}</TableCell>
                        <TableCell className="max-w-[120px] truncate">{row.campaign_name}</TableCell>
                        <TableCell className="max-w-[100px] truncate">{row.ad_set}</TableCell>
                        <TableCell className="max-w-[120px] truncate">{row.ad_name}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{row.platform}</Badge>
                        </TableCell>
                        <TableCell>{row.placement}</TableCell>
                        <TableCell className="text-right">{row.impressions.toLocaleString()}</TableCell>
                        <TableCell className="text-right">{row.reach.toLocaleString()}</TableCell>
                        <TableCell className="text-right">{row.clicks}</TableCell>
                        <TableCell className="text-right">{row.ctr}%</TableCell>
                        <TableCell className="text-right">₹{row.cpc}</TableCell>
                        <TableCell className="text-right font-medium">₹{row.cost.toLocaleString()}</TableCell>
                        <TableCell className="text-right">{row.conversions}</TableCell>
                        <TableCell className="text-right">{row.conversion_rate}%</TableCell>
                        <TableCell className="text-right">₹{row.cpa}</TableCell>
                        <TableCell className="text-right">
                          <Badge variant={row.roas >= 4 ? 'default' : row.roas >= 3 ? 'secondary' : 'destructive'}>
                            {row.roas}x
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right">{row.engagement_rate}%</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Shiprocket Data Tab */}
        <TabsContent value="shiprocket">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center">
                  <Truck className="h-5 w-5 mr-2" />
                  Shiprocket Logistics Data
                </div>
                <Badge variant="outline">{shiprocketData.length} records</Badge>
              </CardTitle>
              <CardDescription>
                Complete shipping and delivery tracking information
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Date</TableHead>
                      <TableHead>Order ID</TableHead>
                      <TableHead>AWB</TableHead>
                      <TableHead>Courier</TableHead>
                      <TableHead>Pickup Date</TableHead>
                      <TableHead>Delivery Date</TableHead>
                      <TableHead>Origin</TableHead>
                      <TableHead>Destination</TableHead>
                      <TableHead className="text-right">Weight (kg)</TableHead>
                      <TableHead>Dimensions</TableHead>
                      <TableHead className="text-right cursor-pointer" onClick={() => handleSort('shipping_cost')}>
                        Shipping Cost <ArrowUpDown className="ml-1 h-4 w-4 inline" />
                      </TableHead>
                      <TableHead className="text-right">COD Amount</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-right">Delivery Days</TableHead>
                      <TableHead className="text-right">Attempts</TableHead>
                      <TableHead>RTO</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {shiprocketData.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell className="font-medium">{row.date}</TableCell>
                        <TableCell className="font-mono text-sm">{row.order_id}</TableCell>
                        <TableCell className="font-mono text-sm">{row.awb}</TableCell>
                        <TableCell>{row.courier}</TableCell>
                        <TableCell>{row.pickup_date}</TableCell>
                        <TableCell>{row.delivery_date || '-'}</TableCell>
                        <TableCell>{row.origin}</TableCell>
                        <TableCell>{row.destination}</TableCell>
                        <TableCell className="text-right">{row.weight}</TableCell>
                        <TableCell className="font-mono text-sm">{row.dimensions}</TableCell>
                        <TableCell className="text-right">₹{row.shipping_cost}</TableCell>
                        <TableCell className="text-right">
                          {row.cod_amount > 0 ? `₹${row.cod_amount.toLocaleString()}` : '-'}
                        </TableCell>
                        <TableCell>
                          <Badge variant={
                            row.status === 'Delivered' ? 'default' : 
                            row.status === 'In Transit' ? 'secondary' : 
                            'destructive'
                          }>
                            {row.status}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right">{row.delivery_time || '-'}</TableCell>
                        <TableCell className="text-right">{row.attempts}</TableCell>
                        <TableCell>
                          {row.rto ? (
                            <Badge variant="destructive">Yes</Badge>
                          ) : (
                            <Badge variant="outline">No</Badge>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}