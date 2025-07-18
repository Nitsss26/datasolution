'use client'

import { useState, useRef, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { 
  Sparkles, 
  Send, 
  Bot, 
  User, 
  Code, 
  BarChart3, 
  Download,
  Copy,
  Check,
  Loader2
} from 'lucide-react'
import { Textarea } from '@/components/ui/textarea'
import type { DashboardData, AIQuery } from '@/types/analytics'

interface AIAssistantProps {
  data?: DashboardData
  onQuery: (query: string) => Promise<{ response: string; sqlQuery?: string }>
  isProcessing: boolean
}

interface ChatMessage {
  id: string
  type: 'user' | 'assistant'
  content: string
  sqlQuery?: string
  timestamp: Date
  hasChart?: boolean
}

const SUGGESTED_QUERIES = [
  "Show me revenue trends for the last 30 days",
  "What's my ROAS across all platforms?",
  "Compare Shopify vs Facebook Ads performance",
  "Generate P&L report for selected platforms",
  "Which products have the highest AOV?",
  "Show delivery performance metrics",
  "What's my customer acquisition cost trend?",
  "Create a funnel analysis for ad campaigns"
]

export function AIAssistant({ data, onQuery, isProcessing }: AIAssistantProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'assistant',
      content: "Hi! I'm your AI analytics assistant. I can help you analyze your D2C data, create custom reports, and answer questions about your business performance. What would you like to know?",
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const scrollAreaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim() || isProcessing) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')

    try {
      const result = await onQuery(input)
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: result.response,
        sqlQuery: result.sqlQuery,
        timestamp: new Date(),
        hasChart: result.response.toLowerCase().includes('chart') || result.response.toLowerCase().includes('graph')
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: "I'm sorry, I encountered an error processing your request. Please try again or rephrase your question.",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleSuggestedQuery = (query: string) => {
    setInput(query)
  }

  const handleCopySQL = async (sql: string, messageId: string) => {
    await navigator.clipboard.writeText(sql)
    setCopiedId(messageId)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <Card className="h-[800px] flex flex-col">
      <CardHeader className="flex flex-row items-center space-y-0 pb-2">
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-purple-500" />
          <CardTitle>AI Assistant</CardTitle>
        </div>
        <Badge variant="outline" className="ml-auto">
          Powered by Gemini
        </Badge>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-0">
        {/* Chat Messages */}
        <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`flex gap-3 max-w-[80%] ${
                    message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
                  }`}
                >
                  <div className="flex-shrink-0">
                    {message.type === 'user' ? (
                      <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                        <User className="h-4 w-4 text-primary-foreground" />
                      </div>
                    ) : (
                      <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                        <Bot className="h-4 w-4 text-white" />
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-col gap-2">
                    <div
                      className={`rounded-lg p-3 ${
                        message.type === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted'
                      }`}
                    >
                      <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    </div>
                    
                    {message.sqlQuery && (
                      <div className="bg-slate-900 text-slate-100 rounded-lg p-3 text-xs font-mono">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <Code className="h-3 w-3" />
                            <span className="text-slate-400">Generated SQL</span>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleCopySQL(message.sqlQuery!, message.id)}
                            className="h-6 w-6 p-0 text-slate-400 hover:text-slate-100"
                          >
                            {copiedId === message.id ? (
                              <Check className="h-3 w-3" />
                            ) : (
                              <Copy className="h-3 w-3" />
                            )}
                          </Button>
                        </div>
                        <pre className="whitespace-pre-wrap">{message.sqlQuery}</pre>
                      </div>
                    )}
                    
                    {message.hasChart && (
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="text-xs">
                          <BarChart3 className="h-3 w-3 mr-1" />
                          View Chart
                        </Button>
                        <Button variant="outline" size="sm" className="text-xs">
                          <Download className="h-3 w-3 mr-1" />
                          Export
                        </Button>
                      </div>
                    )}
                    
                    <span className="text-xs text-muted-foreground">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
            
            {isProcessing && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                  <Bot className="h-4 w-4 text-white" />
                </div>
                <div className="bg-muted rounded-lg p-3">
                  <div className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span className="text-sm">Analyzing your data...</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        <Separator />

        {/* Suggested Queries */}
        <div className="p-4 border-b">
          <h4 className="text-sm font-medium mb-2">Suggested Questions</h4>
          <div className="flex flex-wrap gap-2">
            {SUGGESTED_QUERIES.slice(0, 4).map((query, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                onClick={() => handleSuggestedQuery(query)}
                className="text-xs h-7"
                disabled={isProcessing}
              >
                {query}
              </Button>
            ))}
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4">
          <div className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about your data..."
              className="min-h-[60px] resize-none"
              disabled={isProcessing}
            />
            <Button
              onClick={handleSendMessage}
              disabled={!input.trim() || isProcessing}
              size="sm"
              className="self-end"
            >
              {isProcessing ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </CardContent>
    </Card>
  )
}