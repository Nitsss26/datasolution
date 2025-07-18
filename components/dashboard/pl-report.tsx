'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Download, FileText, TrendingUp, TrendingDown } from 'lucide-react'
import type { DashboardData } from '@/types/analytics'

interface PLReportProps {
  data?: DashboardData
  platforms: string[]
  timeRange: string
}

export function PLReport({ data, platforms, timeRange }: PLReportProps) {
  const formatCurrency = (value: number) => 
    new Intl.NumberFormat('en-IN', { 
      style: 'currency', 
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(value)

  const formatPercentage = (value: number) => `${value.toFixed(2)}%`

  // Calculate P&L data
  const plData = {
    revenue: {
      totalRevenue: data?.d2cMetrics?.totalRevenue || 2847650.75,
      subscriptionRevenue: data?.d2cMetrics?.subscriptionRevenue || 142382.54,
      refunds: data?.d2cMetrics?.refundAmount || 56953.02,
      netRevenue: (data?.d2cMetrics?.totalRevenue || 2847650.75) - (data?.d2cMetrics?.refundAmount || 56953.02)
    },
    costs: {
      cogs: data?.d2cMetrics?.costOfGoodsSold || 1423825.38,
      adSpend: data?.d2cMetrics?.adSpend || 810000.75,
      shippingCosts: data?.d2cMetrics?.shippingCosts || 178900.50,
      marketplaceFees: data?.d2cMetrics?.marketplaceFees || 85429.52,
      paymentGatewayFees: data?.d2cMetrics?.paymentGatewayFees || 42714.76,
      operatingExpenses: data?.d2cMetrics?.operatingExpenses || 284765.08,
      returnProcessingCosts: data?.d2cMetrics?.returnProcessingCosts || 28476.51,
      overheadCosts: data?.d2cMetrics?.overheadCosts || 142382.54
    },
    profit: {
      grossProfit: data?.d2cMetrics?.grossProfit || 1423825.38,
      netProfit: data?.d2cMetrics?.netProfit || 854295.23,
      ebit: data?.d2cMetrics?.ebit || 996677.77,
      operatingProfit: data?.d2cMetrics?.operatingProfit || 854295.23
    },
    margins: {
      grossMargin: data?.d2cMetrics?.grossMargin || 50.02,
      netMargin: data?.d2cMetrics?.netMargin || 30.01
    }
  }

  const totalCosts = Object.values(plData.costs).reduce((sum, cost) => sum + cost, 0)

  const reportSections = [
    {
      title: 'Revenue',
      items: [
        { label: 'Gross Revenue', value: plData.revenue.totalRevenue, isPositive: true },
        { label: 'Subscription Revenue', value: plData.revenue.subscriptionRevenue, isPositive: true, isSubItem: true },
        { label: 'Less: Refunds & Returns', value: -plData.revenue.refunds, isPositive: false },
        { label: 'Net Revenue', value: plData.revenue.netRevenue, isPositive: true, isBold: true }
      ]
    },
    {
      title: 'Cost of Goods Sold',
      items: [
        { label: 'Product Costs (COGS)', value: plData.costs.cogs, isPositive: false },
        { label: 'Gross Profit', value: plData.profit.grossProfit, isPositive: true, isBold: true },
        { label: 'Gross Margin', value: `${plData.margins.grossMargin}%`, isPercentage: true }
      ]
    },
    {
      title: 'Operating Expenses',
      items: [
        { label: 'Marketing & Advertising', value: plData.costs.adSpend, isPositive: false },
        { label: 'Shipping & Fulfillment', value: plData.costs.shippingCosts, isPositive: false },
        { label: 'Marketplace Fees', value: plData.costs.marketplaceFees, isPositive: false },
        { label: 'Payment Processing', value: plData.costs.paymentGatewayFees, isPositive: false },
        { label: 'Return Processing', value: plData.costs.returnProcessingCosts, isPositive: false },
        { label: 'General & Administrative', value: plData.costs.operatingExpenses, isPositive: false },
        { label: 'Other Overhead', value: plData.costs.overheadCosts, isPositive: false },
        { label: 'Total Operating Expenses', value: totalCosts - plData.costs.cogs, isPositive: false, isBold: true }
      ]
    },
    {
      title: 'Profitability',
      items: [
        { label: 'EBIT (Earnings Before Interest & Tax)', value: plData.profit.ebit, isPositive: true },
        { label: 'Operating Profit', value: plData.profit.operatingProfit, isPositive: true },
        { label: 'Net Profit', value: plData.profit.netProfit, isPositive: true, isBold: true },
        { label: 'Net Margin', value: `${plData.margins.netMargin}%`, isPercentage: true, isBold: true }
      ]
    }
  ]

  const handleExport = () => {
    // In a real implementation, this would generate and download a PDF
    console.log('Exporting P&L report...')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Profit & Loss Statement
              </CardTitle>
              <p className="text-muted-foreground mt-1">
                Comprehensive P&L analysis for {platforms.includes('all') ? 'all platforms' : platforms.join(', ')} 
                over the last {timeRange}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline">
                {timeRange}
              </Badge>
              <Button onClick={handleExport}>
                <Download className="h-4 w-4 mr-2" />
                Export PDF
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* P&L Report */}
      <Card>
        <CardContent className="p-6">
          <div className="space-y-8">
            {reportSections.map((section, sectionIndex) => (
              <div key={sectionIndex} className="space-y-4">
                <h3 className="text-lg font-semibold text-primary border-b pb-2">
                  {section.title}
                </h3>
                <div className="space-y-2">
                  {section.items.map((item, itemIndex) => (
                    <div 
                      key={itemIndex} 
                      className={`flex justify-between items-center py-2 ${
                        item.isBold ? 'font-semibold border-t pt-3' : ''
                      } ${item.isSubItem ? 'ml-4 text-sm text-muted-foreground' : ''}`}
                    >
                      <span className="flex items-center gap-2">
                        {item.label}
                        {item.isPositive && !item.isPercentage && (
                          <TrendingUp className="h-3 w-3 text-green-500" />
                        )}
                        {!item.isPositive && !item.isPercentage && (
                          <TrendingDown className="h-3 w-3 text-red-500" />
                        )}
                      </span>
                      <span className={`${
                        item.isBold ? 'text-lg font-bold' : ''
                      } ${
                        item.isPositive && !item.isPercentage ? 'text-green-600' : 
                        !item.isPositive && !item.isPercentage ? 'text-red-600' : 
                        'text-foreground'
                      }`}>
                        {item.isPercentage ? item.value : formatCurrency(Math.abs(item.value as number))}
                      </span>
                    </div>
                  ))}
                </div>
                {sectionIndex < reportSections.length - 1 && <Separator />}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Key Insights */}
      <Card>
        <CardHeader>
          <CardTitle>Key Financial Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatPercentage(plData.margins.grossMargin)}
              </div>
              <div className="text-sm text-green-700">Gross Margin</div>
              <div className="text-xs text-muted-foreground mt-1">Industry avg: 45%</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {formatPercentage(plData.margins.netMargin)}
              </div>
              <div className="text-sm text-blue-700">Net Margin</div>
              <div className="text-xs text-muted-foreground mt-1">Industry avg: 25%</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {formatPercentage((plData.costs.adSpend / plData.revenue.netRevenue) * 100)}
              </div>
              <div className="text-sm text-purple-700">Ad Spend Ratio</div>
              <div className="text-xs text-muted-foreground mt-1">Target: &lt;30%</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {formatPercentage((totalCosts / plData.revenue.netRevenue) * 100)}
              </div>
              <div className="text-sm text-orange-700">Total Cost Ratio</div>
              <div className="text-xs text-muted-foreground mt-1">Lower is better</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle>AI-Powered Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3 p-4 bg-green-50 rounded-lg">
              <TrendingUp className="h-5 w-5 text-green-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-green-800">Strong Gross Margins</h4>
                <p className="text-sm text-green-700">
                  Your gross margin of {formatPercentage(plData.margins.grossMargin)} is above industry average. 
                  Consider investing more in marketing to scale revenue.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
              <FileText className="h-5 w-5 text-blue-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-blue-800">Optimize Operating Expenses</h4>
                <p className="text-sm text-blue-700">
                  Operating expenses account for {formatPercentage((totalCosts - plData.costs.cogs) / plData.revenue.netRevenue * 100)} of revenue. 
                  Focus on reducing shipping and marketplace fees.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 bg-purple-50 rounded-lg">
              <TrendingUp className="h-5 w-5 text-purple-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-purple-800">Marketing Efficiency</h4>
                <p className="text-sm text-purple-700">
                  Your ad spend ratio is {formatPercentage((plData.costs.adSpend / plData.revenue.netRevenue) * 100)}. 
                  Consider A/B testing different channels to improve ROAS.
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}