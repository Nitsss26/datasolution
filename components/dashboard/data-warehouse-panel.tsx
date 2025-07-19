'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { 
  Database, 
  Upload, 
  Download, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  FileJson,
  Table,
  Play,
  Copy,
  ExternalLink,
  Settings,
  Zap
} from 'lucide-react'

interface DataSource {
  id: string
  name: string
  type: string
  status: 'connected' | 'syncing' | 'error'
  lastSync: string
  records: number
  tables: string[]
}

const dataSources: DataSource[] = [
  {
    id: 'shopify',
    name: 'Shopify Store',
    type: 'E-commerce',
    status: 'connected',
    lastSync: '2 minutes ago',
    records: 125430,
    tables: ['orders', 'customers', 'products', 'inventory', 'transactions']
  },
  {
    id: 'google_ads',
    name: 'Google Ads',
    type: 'Advertising',
    status: 'connected',
    lastSync: '5 minutes ago',
    records: 45280,
    tables: ['campaigns', 'ad_groups', 'keywords', 'ads', 'performance']
  },
  {
    id: 'meta_ads',
    name: 'Meta Ads',
    type: 'Advertising',
    status: 'syncing',
    lastSync: 'syncing...',
    records: 38920,
    tables: ['campaigns', 'ad_sets', 'ads', 'insights', 'audiences']
  },
  {
    id: 'shiprocket',
    name: 'Shiprocket',
    type: 'Logistics',
    status: 'connected',
    lastSync: '1 minute ago',
    records: 89340,
    tables: ['shipments', 'tracking', 'returns', 'couriers', 'zones']
  }
]

const bigQueryTables = [
  { name: 'shopify_orders', records: 25430, lastUpdated: '2 min ago', size: '2.3 GB' },
  { name: 'shopify_customers', records: 8540, lastUpdated: '2 min ago', size: '450 MB' },
  { name: 'google_ads_performance', records: 45280, lastUpdated: '5 min ago', size: '1.2 GB' },
  { name: 'meta_ads_insights', records: 38920, lastUpdated: '3 min ago', size: '980 MB' },
  { name: 'shiprocket_shipments', records: 89340, lastUpdated: '1 min ago', size: '3.1 GB' },
]

export function DataWarehousePanel() {
  const [selectedQuery, setSelectedQuery] = useState('')
  const [queryResult, setQueryResult] = useState<any>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const sampleQueries = [
    {
      name: 'Revenue by Platform',
      query: `SELECT 
  platform,
  SUM(revenue) as total_revenue,
  COUNT(DISTINCT order_id) as total_orders
FROM \`project.dataset.unified_orders\`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY platform
ORDER BY total_revenue DESC`
    },
    {
      name: 'Top Products Performance',
      query: `SELECT 
  product_name,
  SUM(quantity) as units_sold,
  SUM(revenue) as total_revenue,
  AVG(price) as avg_price
FROM \`project.dataset.product_sales\`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10`
    },
    {
      name: 'Marketing ROI Analysis',
      query: `SELECT 
  campaign_name,
  platform,
  SUM(spend) as total_spend,
  SUM(revenue) as total_revenue,
  ROUND(SUM(revenue) / SUM(spend), 2) as roas
FROM \`project.dataset.marketing_performance\`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY campaign_name, platform
HAVING total_spend > 1000
ORDER BY roas DESC`
    }
  ]

  const runQuery = async () => {
    if (!selectedQuery.trim()) return
    
    setIsRunning(true)
    // Simulate query execution
    setTimeout(() => {
      setQueryResult({
        rows: [
          { platform: 'Shopify', total_revenue: 1250000, total_orders: 2450 },
          { platform: 'Amazon', total_revenue: 850000, total_orders: 1680 },
          { platform: 'Direct', total_revenue: 420000, total_orders: 890 }
        ],
        executionTime: '2.3s',
        bytesProcessed: '1.2 GB'
      })
      setIsRunning(false)
    }, 2000)
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      // Simulate upload progress
      setUploadProgress(0)
      const interval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval)
            return 100
          }
          return prev + 10
        })
      }, 200)
    }
  }

  return (
    <div className="space-y-6">
      {/* Data Warehouse Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Records</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2.4M+</div>
            <div className="text-xs text-green-600">+12% this month</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Storage Used</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8.2 GB</div>
            <div className="text-xs text-gray-600">of 100 GB limit</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Active Tables</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24</div>
            <div className="text-xs text-blue-600">across 4 sources</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Query Credits</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">847</div>
            <div className="text-xs text-gray-600">remaining this month</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="sources" className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="sources">Data Sources</TabsTrigger>
          <TabsTrigger value="tables">Tables</TabsTrigger>
          <TabsTrigger value="query">Query Builder</TabsTrigger>
          <TabsTrigger value="upload">Upload Data</TabsTrigger>
          <TabsTrigger value="export">Export</TabsTrigger>
        </TabsList>

        {/* Data Sources Tab */}
        <TabsContent value="sources" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Database className="h-5 w-5 mr-2" />
                Connected Data Sources
              </CardTitle>
              <CardDescription>
                Manage your data pipeline connections and sync status
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dataSources.map((source) => (
                  <div key={source.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        {source.status === 'connected' && <CheckCircle className="h-5 w-5 text-green-500" />}
                        {source.status === 'syncing' && <Clock className="h-5 w-5 text-yellow-500 animate-pulse" />}
                        {source.status === 'error' && <AlertCircle className="h-5 w-5 text-red-500" />}
                        <div>
                          <div className="font-medium">{source.name}</div>
                          <div className="text-sm text-gray-500">{source.type}</div>
                        </div>
                      </div>
                      <Badge variant="outline">
                        {source.records.toLocaleString()} records
                      </Badge>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="text-sm text-gray-500">
                        Last sync: {source.lastSync}
                      </div>
                      <Button size="sm" variant="outline">
                        <RefreshCw className="h-4 w-4 mr-1" />
                        Sync
                      </Button>
                      <Button size="sm" variant="outline">
                        <Settings className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tables Tab */}
        <TabsContent value="tables" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Table className="h-5 w-5 mr-2" />
                BigQuery Tables
              </CardTitle>
              <CardDescription>
                Browse and manage your data warehouse tables
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-2">Table Name</th>
                      <th className="text-right p-2">Records</th>
                      <th className="text-right p-2">Size</th>
                      <th className="text-right p-2">Last Updated</th>
                      <th className="text-right p-2">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {bigQueryTables.map((table) => (
                      <tr key={table.name} className="border-b hover:bg-gray-50">
                        <td className="p-2 font-medium">{table.name}</td>
                        <td className="p-2 text-right">{table.records.toLocaleString()}</td>
                        <td className="p-2 text-right">{table.size}</td>
                        <td className="p-2 text-right text-sm text-gray-500">{table.lastUpdated}</td>
                        <td className="p-2 text-right">
                          <div className="flex justify-end space-x-1">
                            <Button size="sm" variant="ghost">
                              <ExternalLink className="h-4 w-4" />
                            </Button>
                            <Button size="sm" variant="ghost">
                              <Download className="h-4 w-4" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Query Builder Tab */}
        <TabsContent value="query" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Database className="h-5 w-5 mr-2" />
                  SQL Query Builder
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="query">SQL Query</Label>
                  <Textarea
                    id="query"
                    placeholder="Enter your BigQuery SQL here..."
                    value={selectedQuery}
                    onChange={(e) => setSelectedQuery(e.target.value)}
                    className="min-h-[200px] font-mono text-sm"
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <Button onClick={runQuery} disabled={isRunning}>
                    {isRunning ? (
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    ) : (
                      <Play className="h-4 w-4 mr-2" />
                    )}
                    Run Query
                  </Button>
                  <Button variant="outline">
                    <Copy className="h-4 w-4 mr-2" />
                    Copy
                  </Button>
                  <Button variant="outline">
                    <Download className="h-4 w-4 mr-2" />
                    Export Results
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Sample Queries</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {sampleQueries.map((query, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      className="w-full justify-start text-left h-auto p-3"
                      onClick={() => setSelectedQuery(query.query)}
                    >
                      <div>
                        <div className="font-medium">{query.name}</div>
                        <div className="text-xs text-gray-500 mt-1">
                          Click to load query
                        </div>
                      </div>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Query Results */}
          {queryResult && (
            <Card>
              <CardHeader>
                <CardTitle>Query Results</CardTitle>
                <CardDescription>
                  Executed in {queryResult.executionTime} • Processed {queryResult.bytesProcessed}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b">
                        {Object.keys(queryResult.rows[0] || {}).map((key) => (
                          <th key={key} className="text-left p-2 font-medium">
                            {key.replace(/_/g, ' ').toUpperCase()}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {queryResult.rows.map((row: any, index: number) => (
                        <tr key={index} className="border-b">
                          {Object.values(row).map((value: any, cellIndex) => (
                            <td key={cellIndex} className="p-2">
                              {typeof value === 'number' ? value.toLocaleString() : value}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Upload Data Tab */}
        <TabsContent value="upload" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Upload className="h-5 w-5 mr-2" />
                Upload Data to BigQuery
              </CardTitle>
              <CardDescription>
                Upload CSV, JSON, or Parquet files to your data warehouse
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="dataset">Dataset</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select dataset" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="analytics">analytics</SelectItem>
                      <SelectItem value="raw_data">raw_data</SelectItem>
                      <SelectItem value="processed">processed</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="table">Table Name</Label>
                  <Input placeholder="Enter table name" />
                </div>
              </div>
              
              <div>
                <Label htmlFor="file">Select File</Label>
                <Input
                  id="file"
                  type="file"
                  accept=".csv,.json,.parquet"
                  onChange={handleFileUpload}
                  className="cursor-pointer"
                />
              </div>

              {uploadProgress > 0 && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Upload Progress</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <Progress value={uploadProgress} />
                </div>
              )}

              <div className="flex items-center space-x-2">
                <Button>
                  <Upload className="h-4 w-4 mr-2" />
                  Upload File
                </Button>
                <Button variant="outline">
                  <FileJson className="h-4 w-4 mr-2" />
                  Upload JSON Schema
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Export Tab */}
        <TabsContent value="export" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Download className="h-5 w-5 mr-2" />
                Export Data
              </CardTitle>
              <CardDescription>
                Export your data in various formats for external analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Export Format</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select format" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="csv">CSV</SelectItem>
                      <SelectItem value="json">JSON</SelectItem>
                      <SelectItem value="excel">Excel</SelectItem>
                      <SelectItem value="parquet">Parquet</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Date Range</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select range" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="7d">Last 7 days</SelectItem>
                      <SelectItem value="30d">Last 30 days</SelectItem>
                      <SelectItem value="90d">Last 90 days</SelectItem>
                      <SelectItem value="custom">Custom range</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Button className="h-20 flex-col">
                  <Download className="h-6 w-6 mb-2" />
                  Export All Data
                </Button>
                <Button variant="outline" className="h-20 flex-col">
                  <Table className="h-6 w-6 mb-2" />
                  Export Specific Tables
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}