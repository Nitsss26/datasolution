'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { 
  Search, 
  Filter, 
  Download, 
  RefreshCw,
  Database,
  Eye,
  MoreHorizontal
} from 'lucide-react'

interface DataTable {
  id: string
  name: string
  platform: string
  records: number
  lastUpdated: string
  status: 'active' | 'syncing' | 'error'
  description: string
}

interface DataRecord {
  id: string
  [key: string]: any
}

export default function DataTablesPage() {
  const [tables, setTables] = useState<DataTable[]>([
    {
      id: 'shopify_orders',
      name: 'Orders',
      platform: 'Shopify',
      records: 8945,
      lastUpdated: '2 minutes ago',
      status: 'active',
      description: 'Customer orders with line items and fulfillment data'
    },
    {
      id: 'shopify_customers',
      name: 'Customers',
      platform: 'Shopify',
      records: 3421,
      lastUpdated: '2 minutes ago',
      status: 'active',
      description: 'Customer profiles with contact and purchase history'
    },
    {
      id: 'shopify_products',
      name: 'Products',
      platform: 'Shopify',
      records: 245,
      lastUpdated: '5 minutes ago',
      status: 'active',
      description: 'Product catalog with variants and inventory'
    },
    {
      id: 'facebook_campaigns',
      name: 'Ad Campaigns',
      platform: 'Facebook',
      records: 1250,
      lastUpdated: '3 minutes ago',
      status: 'active',
      description: 'Campaign performance metrics and audience data'
    },
    {
      id: 'google_campaigns',
      name: 'Ad Campaigns',
      platform: 'Google Ads',
      records: 850,
      lastUpdated: '5 minutes ago',
      status: 'active',
      description: 'Keyword performance and campaign analytics'
    },
    {
      id: 'shiprocket_shipments',
      name: 'Shipments',
      platform: 'Shiprocket',
      records: 7234,
      lastUpdated: '1 minute ago',
      status: 'active',
      description: 'Shipping tracking and delivery performance'
    }
  ])

  const [selectedTable, setSelectedTable] = useState<string | null>(null)
  const [tableData, setTableData] = useState<DataRecord[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPlatform, setSelectedPlatform] = useState('all')
  const [isLoading, setIsLoading] = useState(false)

  const platforms = ['all', ...Array.from(new Set(tables.map(t => t.platform)))]

  const filteredTables = tables.filter(table => {
    const matchesSearch = table.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         table.platform.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesPlatform = selectedPlatform === 'all' || table.platform === selectedPlatform
    return matchesSearch && matchesPlatform
  })

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800">Active</Badge>
      case 'syncing':
        return <Badge className="bg-blue-100 text-blue-800">Syncing</Badge>
      case 'error':
        return <Badge variant="destructive">Error</Badge>
      default:
        return <Badge variant="secondary">Unknown</Badge>
    }
  }

  const handleViewTable = async (tableId: string) => {
    setSelectedTable(tableId)
    setIsLoading(true)
    
    // Simulate loading table data
    setTimeout(() => {
      // Generate mock data based on table type
      const mockData = generateMockData(tableId)
      setTableData(mockData)
      setIsLoading(false)
    }, 1000)
  }

  const generateMockData = (tableId: string): DataRecord[] => {
    switch (tableId) {
      case 'shopify_orders':
        return Array.from({ length: 10 }, (_, i) => ({
          id: `order_${i + 1}`,
          order_number: `#${1000 + i}`,
          customer_email: `customer${i + 1}@example.com`,
          total_price: `₹${(Math.random() * 5000 + 500).toFixed(2)}`,
          created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toLocaleDateString(),
          financial_status: Math.random() > 0.8 ? 'pending' : 'paid',
          fulfillment_status: Math.random() > 0.7 ? 'unfulfilled' : 'fulfilled'
        }))
      
      case 'shopify_customers':
        return Array.from({ length: 10 }, (_, i) => ({
          id: `customer_${i + 1}`,
          email: `customer${i + 1}@example.com`,
          first_name: `Customer${i + 1}`,
          last_name: 'Demo',
          orders_count: Math.floor(Math.random() * 10) + 1,
          total_spent: `₹${(Math.random() * 10000 + 1000).toFixed(2)}`,
          created_at: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toLocaleDateString(),
          accepts_marketing: Math.random() > 0.5 ? 'Yes' : 'No'
        }))
      
      case 'facebook_campaigns':
        return Array.from({ length: 10 }, (_, i) => ({
          id: `campaign_${i + 1}`,
          campaign_name: `Campaign ${i + 1}`,
          impressions: Math.floor(Math.random() * 100000) + 10000,
          clicks: Math.floor(Math.random() * 5000) + 500,
          spend: `₹${(Math.random() * 50000 + 5000).toFixed(2)}`,
          ctr: `${(Math.random() * 3 + 0.5).toFixed(2)}%`,
          cpc: `₹${(Math.random() * 10 + 2).toFixed(2)}`,
          conversions: Math.floor(Math.random() * 100) + 10,
          roas: `${(Math.random() * 5 + 2).toFixed(2)}x`
        }))
      
      default:
        return Array.from({ length: 10 }, (_, i) => ({
          id: `record_${i + 1}`,
          name: `Record ${i + 1}`,
          value: Math.floor(Math.random() * 1000),
          status: Math.random() > 0.5 ? 'Active' : 'Inactive',
          created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toLocaleDateString()
        }))
    }
  }

  const handleExport = (tableId: string) => {
    // Simulate export
    console.log(`Exporting table: ${tableId}`)
  }

  const handleRefresh = (tableId: string) => {
    setTables(prev => prev.map(t => 
      t.id === tableId 
        ? { ...t, status: 'syncing' as const, lastUpdated: 'Syncing...' }
        : t
    ))

    // Simulate refresh
    setTimeout(() => {
      setTables(prev => prev.map(t => 
        t.id === tableId 
          ? { ...t, status: 'active' as const, lastUpdated: 'Just now' }
          : t
      ))
    }, 2000)
  }

  const totalRecords = tables.reduce((sum, table) => sum + table.records, 0)

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Data Tables</h1>
              <p className="text-muted-foreground mt-1">
                Explore and manage your integrated platform data
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{tables.length}</div>
                <div className="text-sm text-muted-foreground">Tables</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{totalRecords.toLocaleString()}</div>
                <div className="text-sm text-muted-foreground">Records</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="space-y-6">
          {!selectedTable ? (
            <>
              {/* Filters */}
              <Card>
                <CardContent className="p-4">
                  <div className="flex flex-col sm:flex-row gap-4">
                    <div className="relative flex-1">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                      <Input
                        placeholder="Search tables..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                    <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
                      <SelectTrigger className="w-48">
                        <Filter className="h-4 w-4 mr-2" />
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {platforms.map(platform => (
                          <SelectItem key={platform} value={platform}>
                            {platform === 'all' ? 'All Platforms' : platform}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>

              {/* Tables Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {filteredTables.map((table) => (
                  <Card key={table.id} className="hover:shadow-md transition-all duration-200">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className="p-2 bg-blue-100 rounded-lg">
                            <Database className="h-5 w-5 text-blue-600" />
                          </div>
                          <div>
                            <CardTitle className="text-lg">{table.name}</CardTitle>
                            <p className="text-sm text-muted-foreground">{table.platform}</p>
                          </div>
                        </div>
                        {getStatusBadge(table.status)}
                      </div>
                    </CardHeader>
                    
                    <CardContent className="space-y-4">
                      <p className="text-sm text-muted-foreground">
                        {table.description}
                      </p>
                      
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <div className="font-medium text-lg">{table.records.toLocaleString()}</div>
                          <div className="text-muted-foreground">Records</div>
                        </div>
                        <div>
                          <div className="font-medium">{table.lastUpdated}</div>
                          <div className="text-muted-foreground">Last Updated</div>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between pt-2">
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => handleRefresh(table.id)}
                          disabled={table.status === 'syncing'}
                        >
                          <RefreshCw className={`h-4 w-4 mr-2 ${table.status === 'syncing' ? 'animate-spin' : ''}`} />
                          Refresh
                        </Button>
                        
                        <div className="flex items-center gap-2">
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => handleExport(table.id)}
                          >
                            <Download className="h-4 w-4 mr-2" />
                            Export
                          </Button>
                          <Button 
                            size="sm"
                            onClick={() => handleViewTable(table.id)}
                          >
                            <Eye className="h-4 w-4 mr-2" />
                            View Data
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </>
          ) : (
            /* Table Data View */
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Button variant="outline" onClick={() => setSelectedTable(null)}>
                    ← Back to Tables
                  </Button>
                  <h2 className="text-xl font-semibold">
                    {tables.find(t => t.id === selectedTable)?.name} Data
                  </h2>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="outline" size="sm">
                    <Download className="h-4 w-4 mr-2" />
                    Export
                  </Button>
                  <Button variant="outline" size="sm">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                  </Button>
                </div>
              </div>

              <Card>
                <CardContent className="p-0">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-64">
                      <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
                    </div>
                  ) : (
                    <div className="overflow-x-auto">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            {tableData.length > 0 && Object.keys(tableData[0]).map((key) => (
                              <TableHead key={key} className="capitalize">
                                {key.replace(/_/g, ' ')}
                              </TableHead>
                            ))}
                            <TableHead className="w-12"></TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {tableData.map((record, index) => (
                            <TableRow key={index}>
                              {Object.values(record).map((value, cellIndex) => (
                                <TableCell key={cellIndex} className="font-mono text-sm">
                                  {String(value)}
                                </TableCell>
                              ))}
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
                  )}
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}