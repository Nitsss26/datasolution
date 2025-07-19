// Demo Data for D2C Analytics Platform
export const demoData = {
  // Revenue Data (Last 12 months)
  revenueData: [
    { month: 'Jan 2024', revenue: 1850000, orders: 1240, customers: 890, profit: 555000 },
    { month: 'Feb 2024', revenue: 2200000, orders: 1450, customers: 1020, profit: 660000 },
    { month: 'Mar 2024', revenue: 1950000, orders: 1320, customers: 950, profit: 585000 },
    { month: 'Apr 2024', revenue: 2750000, orders: 1680, customers: 1180, profit: 825000 },
    { month: 'May 2024', revenue: 3100000, orders: 1890, customers: 1350, profit: 930000 },
    { month: 'Jun 2024', revenue: 2850000, orders: 1750, customers: 1220, profit: 855000 },
    { month: 'Jul 2024', revenue: 3200000, orders: 1950, customers: 1400, profit: 960000 },
    { month: 'Aug 2024', revenue: 2900000, orders: 1820, customers: 1280, profit: 870000 },
    { month: 'Sep 2024', revenue: 3350000, orders: 2100, customers: 1520, profit: 1005000 },
    { month: 'Oct 2024', revenue: 3800000, orders: 2350, customers: 1680, profit: 1140000 },
    { month: 'Nov 2024', revenue: 4200000, orders: 2580, customers: 1850, profit: 1260000 },
    { month: 'Dec 2024', revenue: 4850000, orders: 2920, customers: 2100, profit: 1455000 },
  ],

  // Platform Revenue Distribution
  platformData: [
    { name: 'Shopify', revenue: 12500000, percentage: 45, color: '#8B5CF6', orders: 8500 },
    { name: 'Amazon', revenue: 8500000, percentage: 30, color: '#3B82F6', orders: 5200 },
    { name: 'Facebook Ads', revenue: 4200000, percentage: 15, color: '#10B981', orders: 2800 },
    { name: 'Google Ads', revenue: 2800000, percentage: 10, color: '#F59E0B', orders: 1900 },
  ],

  // Ad Performance Metrics
  adMetrics: [
    { 
      platform: 'Facebook Ads', 
      spend: 1250000, 
      impressions: 25000000, 
      clicks: 450000, 
      conversions: 18000, 
      roas: 4.2,
      cpc: 2.78,
      ctr: 1.8,
      conversionRate: 4.0
    },
    { 
      platform: 'Google Ads', 
      spend: 980000, 
      impressions: 18000000, 
      clicks: 380000, 
      conversions: 15200, 
      roas: 3.8,
      cpc: 2.58,
      ctr: 2.1,
      conversionRate: 4.0
    },
    { 
      platform: 'Instagram Ads', 
      spend: 750000, 
      impressions: 12000000, 
      clicks: 280000, 
      conversions: 9800, 
      roas: 3.5,
      cpc: 2.68,
      ctr: 2.3,
      conversionRate: 3.5
    },
  ],

  // Delivery Performance
  deliveryMetrics: [
    { 
      courier: 'Shiprocket', 
      orders: 12500, 
      onTime: 94.5, 
      avgTime: 2.3, 
      cost: 1850000,
      returnRate: 2.1,
      customerSatisfaction: 4.6
    },
    { 
      courier: 'Delhivery', 
      orders: 8500, 
      onTime: 92.1, 
      avgTime: 2.8, 
      cost: 1420000,
      returnRate: 2.8,
      customerSatisfaction: 4.3
    },
    { 
      courier: 'BlueDart', 
      orders: 4200, 
      onTime: 96.2, 
      avgTime: 1.9, 
      cost: 980000,
      returnRate: 1.5,
      customerSatisfaction: 4.8
    },
  ],

  // Customer Metrics
  customerMetrics: {
    totalCustomers: 45280,
    newCustomers: 8540,
    returningCustomers: 36740,
    customerAcquisitionCost: 245,
    customerLifetimeValue: 1850,
    repeatPurchaseRate: 34.2,
    churnRate: 12.5,
    averageOrderValue: 1680,
    netPromoterScore: 72
  },

  // Inventory Metrics
  inventoryMetrics: {
    totalProducts: 1250,
    inStock: 1180,
    outOfStock: 70,
    lowStock: 120,
    inventoryValue: 8500000,
    inventoryTurnover: 6.2,
    stockAccuracy: 98.5
  },

  // Financial Summary (P&L)
  financialSummary: {
    totalRevenue: 27850000,
    grossRevenue: 27850000,
    returns: 580000,
    netRevenue: 27270000,
    
    // Costs
    costOfGoodsSold: 11080000,
    adSpend: 2980000,
    shippingCosts: 1850000,
    platformFees: 1260000,
    paymentGatewayFees: 420000,
    operatingExpenses: 950000,
    totalCosts: 18540000,
    
    // Profits
    grossProfit: 16190000,
    operatingProfit: 8730000,
    netProfit: 8730000,
    
    // Margins
    grossMargin: 58.1,
    operatingMargin: 31.4,
    netMargin: 31.4,
    
    // Other metrics
    ebitda: 9200000,
    roi: 47.1,
    paybackPeriod: 2.1
  },

  // Top Products
  topProducts: [
    { name: 'Premium Skincare Set', revenue: 2850000, orders: 1200, margin: 65 },
    { name: 'Wireless Earbuds Pro', revenue: 2400000, orders: 1500, margin: 45 },
    { name: 'Smart Fitness Tracker', revenue: 1950000, orders: 980, margin: 55 },
    { name: 'Organic Tea Collection', revenue: 1680000, orders: 2100, margin: 70 },
    { name: 'Designer Handbag', revenue: 1420000, orders: 450, margin: 80 },
  ],

  // Geographic Performance
  geographicData: [
    { region: 'Mumbai', revenue: 8500000, orders: 4200, percentage: 30.5 },
    { region: 'Delhi', revenue: 6800000, orders: 3400, percentage: 24.4 },
    { region: 'Bangalore', revenue: 5200000, orders: 2800, percentage: 18.7 },
    { region: 'Chennai', revenue: 3400000, orders: 1900, percentage: 12.2 },
    { region: 'Pune', revenue: 2850000, orders: 1500, percentage: 10.2 },
    { region: 'Others', revenue: 1100000, orders: 800, percentage: 4.0 },
  ],

  // Platform Connection Status
  platformStatus: [
    {
      id: 'shopify',
      name: 'Shopify',
      connected: true,
      lastSync: '2 minutes ago',
      status: 'connected',
      dataPoints: 12450,
      health: 'excellent'
    },
    {
      id: 'facebook',
      name: 'Facebook Ads',
      connected: true,
      lastSync: '5 minutes ago',
      status: 'connected',
      dataPoints: 8920,
      health: 'good'
    },
    {
      id: 'google',
      name: 'Google Ads',
      connected: true,
      lastSync: '3 minutes ago',
      status: 'connected',
      dataPoints: 6780,
      health: 'excellent'
    },
    {
      id: 'shiprocket',
      name: 'Shiprocket',
      connected: true,
      lastSync: '1 minute ago',
      status: 'connected',
      dataPoints: 15240,
      health: 'good'
    },
    {
      id: 'amazon',
      name: 'Amazon',
      connected: false,
      lastSync: null,
      status: 'disconnected',
      dataPoints: 0,
      health: 'not_connected'
    },
    {
      id: 'flipkart',
      name: 'Flipkart',
      connected: false,
      lastSync: null,
      status: 'disconnected',
      dataPoints: 0,
      health: 'not_connected'
    }
  ],

  // BigQuery Status
  bigQueryStatus: {
    connected: true,
    projectId: 'd2c-analytics-pro',
    dataset: 'd2c_data',
    location: 'US',
    tablesCount: 12,
    totalRows: 127450,
    lastSync: '2 minutes ago',
    storageUsed: '2.4 GB',
    queriesThisMonth: 1250
  },

  // AI Insights
  aiInsights: [
    {
      type: 'opportunity',
      title: 'Facebook Ads Optimization',
      description: 'Your Facebook ROAS of 4.2x is excellent. Consider increasing budget by 25% for campaigns with ROAS > 4x.',
      impact: 'high',
      category: 'marketing'
    },
    {
      type: 'warning',
      title: 'Inventory Alert',
      description: '70 products are out of stock. This could impact revenue by ₹2.1M this month.',
      impact: 'high',
      category: 'inventory'
    },
    {
      type: 'insight',
      title: 'Customer Retention',
      description: 'Customers from Mumbai have 45% higher LTV. Focus retention campaigns on this segment.',
      impact: 'medium',
      category: 'customers'
    },
    {
      type: 'opportunity',
      title: 'Shipping Optimization',
      description: 'BlueDart has 96.2% on-time delivery. Consider shifting more volume from other couriers.',
      impact: 'medium',
      category: 'operations'
    }
  ]
}

export default demoData