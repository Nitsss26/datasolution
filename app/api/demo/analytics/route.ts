import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { platforms, timeRange } = await request.json()

    // Return comprehensive demo analytics data
    const demoAnalytics = {
      d2cMetrics: {
        totalRevenue: 2847650.75,
        averageOrderValue: 318.45,
        revenuePerChannel: {
          organic: 1138706.30,
          paid: 1423825.38,
          social: 285119.07
        },
        grossMerchandiseValue: 2847650.75,
        subscriptionRevenue: 142382.54,
        refundAmount: 56953.02,
        costOfGoodsSold: 1423825.38,
        operatingExpenses: 284765.08,
        adSpend: 810000.75,
        marketplaceFees: 85429.52,
        shippingCosts: 178900.50,
        paymentGatewayFees: 42714.76,
        returnProcessingCosts: 28476.51,
        overheadCosts: 142382.54,
        grossProfit: 1423825.38,
        netProfit: 854295.23,
        grossMargin: 50.02,
        netMargin: 30.01,
        ebit: 996677.77,
        operatingProfit: 854295.23,
        customerAcquisitionCost: 125.50,
        customerLifetimeValue: 1250.75,
        repeatPurchaseRate: 35.5,
        churnRate: 8.2,
        newCustomerCount: 1368,
        returningCustomerCount: 2053,
        customerRetentionRate: 91.8,
        netPromoterScore: 72,
        avgCustomerSatisfactionScore: 4.3,
        inventoryTurnover: 8.5,
        stockoutRate: 2.1,
        daysToSellInventory: 43,
        inventoryValue: 1423825.38,
        overstockRate: 5.2,
        stockAccuracy: 97.8,
        sessions: 425000,
        bounceRate: 45.2,
        avgSessionDuration: 185,
        pageViews: 1275000,
        uniqueVisitors: 325000,
        exitRate: 38.5,
        pagesPerSession: 3.0,
        timeToFirstByte: 1.2,
        cartAbandonmentRate: 68.5,
        totalOrders: 8945
      },
      adMetrics: {
        impressions: 21250000,
        clicks: 212500,
        clickThroughRate: 1.0,
        costPerClick: 3.81,
        conversions: 7750,
        conversionRate: 3.65,
        costPerConversion: 104.52,
        returnOnAdSpend: 6.98,
        advertisingCostOfSales: 14.32,
        costPerMille: 38.12,
        costPerAction: 104.52,
        likes: 85000,
        shares: 12750,
        comments: 8500,
        videoViews: 1275000,
        videoCompletionRate: 65.5,
        engagementRate: 4.8,
        adReach: 8500000,
        frequency: 2.5,
        qualityScore: 8.2,
        adPosition: 1.8,
        clickToOpenRate: 12.5
      },
      deliveryMetrics: {
        avgDeliveryTime: 3.2,
        shippingCostPerOrder: 20.0,
        onTimeDeliveryRate: 92.05,
        lateDeliveryRate: 7.95,
        failedDeliveryAttempts: 178,
        returnRate: 4.2,
        returnProcessingTime: 2.5,
        pickupSuccessRate: 98.5,
        totalShippingCost: 178900.50,
        fuelSurcharge: 8945.03,
        handlingFees: 4472.51,
        insuranceCosts: 2236.26,
        deliveryDistance: 450.5,
        packageVolume: 8945,
        courierEfficiency: 94.2,
        customerComplaintRate: 1.8,
        averageShippingCost: 20.0,
        totalShipments: 8945,
        averageDeliveryTime: 3.2
      },
      timeSeriesData: Array.from({ length: 30 }, (_, i) => {
        const date = new Date()
        date.setDate(date.getDate() - (29 - i))
        return {
          date: date.toISOString().split('T')[0],
          totalRevenue: Math.floor(Math.random() * 100000) + 50000,
          newCustomerCount: Math.floor(Math.random() * 50) + 20,
          sessions: Math.floor(Math.random() * 5000) + 2000,
          conversions: Math.floor(Math.random() * 200) + 100,
          adSpend: Math.floor(Math.random() * 20000) + 10000,
          grossMargin: Math.random() * 20 + 40,
          orders: Math.floor(Math.random() * 300) + 150,
          aov: Math.floor(Math.random() * 200) + 250,
          cac: Math.floor(Math.random() * 50) + 100,
          roas: Math.random() * 3 + 4,
          deliveryTime: Math.random() * 2 + 2,
          inventoryTurnover: Math.random() * 5 + 6
        }
      }),
      platformBreakdown: {
        shopify: {
          revenue: 2847650.75,
          orders: 8945,
          customers: 3421,
          aov: 318.45,
          conversions: 8945,
          conversionRate: 3.45
        },
        facebook: {
          revenue: 1423825.38,
          cost: 425000.50,
          impressions: 12500000,
          clicks: 125000,
          conversions: 4250,
          roas: 6.70,
          ctr: 1.0,
          avgDeliveryTime: 3.2,
          fees: 85429.52,
          conversionRate: 3.4
        },
        google: {
          revenue: 1138706.30,
          cost: 385000.25,
          impressions: 8750000,
          clicks: 87500,
          conversions: 3500,
          roas: 7.40,
          ctr: 1.0,
          avgDeliveryTime: 3.1,
          fees: 77141.26,
          conversionRate: 4.0
        },
        shiprocket: {
          deliveries: 8945,
          onTime: 8234,
          avgDeliveryTime: 3.2,
          cost: 178900.50,
          fees: 8945.03
        }
      },
      summary: {
        totalRevenue: 2847650.75,
        totalOrders: 8945,
        totalCustomers: 3421,
        roas: 6.98,
        dataPoints: 25000
      }
    }

    return NextResponse.json(demoAnalytics)
  } catch (error) {
    console.error('Demo analytics error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch demo analytics data' },
      { status: 500 }
    )
  }
}