import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json()

    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      )
    }

    // For now, return a mock response
    // In production, this would integrate with Google Gemini AI
    const mockResponse = {
      response: `Based on your query "${query}", here's what I found:

• Your current revenue trends show positive growth
• Customer acquisition metrics are performing well
• Consider optimizing your marketing spend allocation
• Delivery performance has room for improvement

Would you like me to generate a specific report or chart for this analysis?`,
      sqlQuery: `-- Generated SQL for: ${query}
SELECT 
  DATE(created_at) as date,
  SUM(total_price) as revenue,
  COUNT(*) as orders,
  AVG(total_price) as aov
FROM orders 
WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC;`
    }

    return NextResponse.json(mockResponse)
  } catch (error) {
    console.error('AI query error:', error)
    return NextResponse.json(
      { error: 'Failed to process AI query' },
      { status: 500 }
    )
  }
}