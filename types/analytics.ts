// D2C Analytics Types

export interface D2CMetrics {
  // Revenue Metrics (All amounts in INR)
  totalRevenue: number
  averageOrderValue: number
  revenuePerChannel: Record<string, number>
  grossMerchandiseValue: number
  subscriptionRevenue: number
  refundAmount: number
  
  // Cost Metrics (All amounts in INR)
  costOfGoodsSold: number
  operatingExpenses: number
  adSpend: number
  marketplaceFees: number
  shippingCosts: number
  paymentGatewayFees: number
  returnProcessingCosts: number
  overheadCosts: number
  
  // Profit Metrics (All amounts in INR)
  grossProfit: number
  netProfit: number
  grossMargin: number
  netMargin: number
  ebit: number
  operatingProfit: number
  
  // Customer Metrics
  customerAcquisitionCost: number // INR
  customerLifetimeValue: number // INR
  repeatPurchaseRate: number
  churnRate: number
  newCustomerCount: number
  returningCustomerCount: number
  customerRetentionRate: number
  netPromoterScore: number
  avgCustomerSatisfactionScore: number
  
  // Inventory Metrics
  inventoryTurnover: number
  stockoutRate: number
  daysToSellInventory: number
  inventoryValue: number // INR
  overstockRate: number
  stockAccuracy: number
  
  // Website Metrics
  sessions: number
  bounceRate: number
  avgSessionDuration: number
  pageViews: number
  uniqueVisitors: number
  exitRate: number
  pagesPerSession: number
  timeToFirstByte: number
  cartAbandonmentRate: number
  
  // Order Metrics
  totalOrders?: number
}

export interface AdMetrics {
  // Performance Metrics (Costs in INR)
  impressions: number
  clicks: number
  clickThroughRate: number
  costPerClick: number // INR
  conversions: number
  conversionRate: number
  costPerConversion: number // INR
  returnOnAdSpend: number
  advertisingCostOfSales: number
  costPerMille: number // INR
  costPerAction: number // INR
  
  // Engagement Metrics
  likes: number
  shares: number
  comments: number
  videoViews: number
  videoCompletionRate: number
  engagementRate: number
  
  // Campaign-Specific Metrics
  adReach: number
  frequency: number
  qualityScore: number
  adPosition: number
  clickToOpenRate: number
}

export interface DeliveryMetrics {
  // Shipping Metrics
  avgDeliveryTime: number
  shippingCostPerOrder: number // INR
  onTimeDeliveryRate: number
  lateDeliveryRate: number
  failedDeliveryAttempts: number
  returnRate: number
  returnProcessingTime: number
  pickupSuccessRate: number
  
  // Cost Metrics (All amounts in INR)
  totalShippingCost: number
  fuelSurcharge: number
  handlingFees: number
  insuranceCosts: number
  
  // Performance Metrics
  deliveryDistance: number
  packageVolume: number
  courierEfficiency: number
  customerComplaintRate: number
  
  // Additional metrics
  averageShippingCost?: number // INR
  totalShipments?: number
  averageDeliveryTime?: number
}

export interface TimeSeriesDataPoint {
  date: string
  totalRevenue: number // INR
  newCustomerCount: number
  sessions: number
  conversions: number
  adSpend: number // INR
  grossMargin: number
  orders: number
  aov: number // INR
  cac: number // INR
  roas: number
  deliveryTime: number
  inventoryTurnover: number
}

export interface PlatformBreakdown {
  [platform: string]: {
    revenue?: number // INR
    orders?: number
    customers?: number
    aov?: number // INR
    conversions?: number
    roas?: number
    ctr?: number
    deliveries?: number
    onTime?: number
    cost?: number // INR
    avgDeliveryTime?: number
    fees?: number // INR
    conversionRate?: number
  }
}

export interface DashboardData {
  d2cMetrics: D2CMetrics
  adMetrics: AdMetrics
  deliveryMetrics: DeliveryMetrics
  timeSeriesData: TimeSeriesDataPoint[]
  platformBreakdown: PlatformBreakdown
  trends?: {
    revenue?: Array<{ date: string; value: number }>
    orders?: Array<{ date: string; value: number }>
    customers?: Array<{ date: string; value: number }>
    roas?: Array<{ date: string; value: number }>
  }
  summary?: {
    totalRevenue: number // INR
    totalOrders: number
    totalCustomers: number
    roas: number
    dataPoints: number
  }
}

export interface ChartConfig {
  id?: string
  type: 'line' | 'bar' | 'pie' | 'area' | 'gauge' | 'funnel' | 'heatmap' | 'scatter' | 'table'
  title: string
  metric: string
  timeRange?: string
  compareWith?: string
  options?: {
    showLegend?: boolean
    showGrid?: boolean
    showLabels?: boolean
  }
}

export interface UserPreferences {
  selectedPlatforms: string[]
  defaultTimeRange: string
  favoriteCharts: string[]
  theme: 'light' | 'dark' | 'system'
  aiEnabled: boolean
  dashboardLayout?: any[]
}

export interface Platform {
  id: string
  name: string
  connected: boolean
  lastSync?: string
  dataPoints?: number
}

export interface PlatformData {
  platform: string
  data: any
  lastUpdated: string
}

export interface AnalyticsData {
  platforms: string[]
  timeRange: string
  data: DashboardData
  generatedAt: string
}

export interface AIQuery {
  id: string
  query: string
  response: string
  sqlQuery?: string
  timestamp: Date
}