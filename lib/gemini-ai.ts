import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '')

export async function queryGeminiAI(prompt: string, context?: any) {
  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' })

    const contextualPrompt = `
You are an expert D2C analytics assistant. You help analyze business data and provide actionable insights.

Context Data: ${context ? JSON.stringify(context, null, 2) : 'No specific data provided'}

User Query: ${prompt}

Please provide:
1. A clear, actionable response
2. If applicable, suggest a SQL query to extract relevant data
3. Include specific metrics and recommendations
4. Format your response in a helpful, professional manner

Response:
`

    const result = await model.generateContent(contextualPrompt)
    const response = await result.response
    const text = response.text()

    // Try to extract SQL query if present
    const sqlMatch = text.match(/```sql\n([\s\S]*?)\n```/)
    const sqlQuery = sqlMatch ? sqlMatch[1].trim() : undefined

    return {
      response: text,
      sqlQuery
    }
  } catch (error) {
    console.error('Gemini AI Error:', error)
    throw new Error('Failed to process AI query')
  }
}

export async function generateInsights(data: any) {
  const prompt = `
Analyze this D2C business data and provide key insights:

Data Summary:
- Total Revenue: $${data.d2cMetrics?.totalRevenue || 0}
- Net Profit: $${data.d2cMetrics?.netProfit || 0}
- ROAS: ${data.adMetrics?.returnOnAdSpend || 0}x
- Customer Acquisition Cost: $${data.d2cMetrics?.customerAcquisitionCost || 0}
- Customer Lifetime Value: $${data.d2cMetrics?.customerLifetimeValue || 0}

Please provide:
1. Top 3 performance insights
2. 2-3 actionable recommendations
3. Key areas of concern (if any)
4. Growth opportunities

Keep it concise and actionable.
`

  return await queryGeminiAI(prompt, data)
}

export async function generateSQLQuery(naturalLanguageQuery: string, schema?: any) {
  const prompt = `
Convert this natural language query to SQL for a D2C analytics database:

Query: "${naturalLanguageQuery}"

Database Schema Context:
- orders table: id, customer_id, total_amount, created_at, platform, status
- customers table: id, email, created_at, lifetime_value, acquisition_cost
- ad_campaigns table: id, platform, spend, impressions, clicks, conversions, date
- products table: id, name, price, category, inventory_count
- shipments table: id, order_id, status, delivery_date, cost

Generate a SQL query that would answer this question. Only return the SQL query without explanation.
`

  const result = await queryGeminiAI(prompt, schema)
  return result.sqlQuery || result.response
}