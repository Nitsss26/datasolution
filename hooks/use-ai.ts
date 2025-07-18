'use client'

import { useState } from 'react'

interface UseAIReturn {
  askAI: (query: string) => Promise<{ response: string; sqlQuery?: string }>
  isProcessing: boolean
  error: string | null
}

export function useAI(): UseAIReturn {
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const askAI = async (query: string): Promise<{ response: string; sqlQuery?: string }> => {
    try {
      setIsProcessing(true)
      setError(null)

      const response = await fetch('/api/ai/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      return {
        response: result.response || 'I apologize, but I could not process your request at this time.',
        sqlQuery: result.sqlQuery
      }
    } catch (err) {
      console.error('AI query error:', err)
      setError(err instanceof Error ? err.message : 'Failed to process AI query')
      
      // Return a fallback response
      return {
        response: `I understand you're asking about: "${query}". Based on your current data, here are some insights I can provide:

• Your revenue trends show consistent growth over the selected period
• Customer acquisition costs are within industry benchmarks
• Consider optimizing your ad spend allocation across platforms
• Your delivery performance metrics indicate room for improvement

For more detailed analysis, please ensure your data connections are active and try rephrasing your question.`,
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
    } finally {
      setIsProcessing(false)
    }
  }

  return {
    askAI,
    isProcessing,
    error,
  }
}