'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ScrollArea } from '@/components/ui/scroll-area'
import { 
  MessageSquare, 
  Send, 
  Bot, 
  User, 
  TrendingUp, 
  AlertTriangle, 
  Lightbulb,
  BarChart3,
  Target,
  DollarSign,
  Users,
  Zap,
  Brain,
  Sparkles
} from 'lucide-react'

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  suggestions?: string[]
}

interface Insight {
  id: string
  type: 'opportunity' | 'warning' | 'trend' | 'recommendation'
  title: string
  description: string
  impact: 'high' | 'medium' | 'low'
  metric: string
  value: string
  change: string
}

const aiInsights: Insight[] = [
  {
    id: '1',
    type: 'opportunity',
    title: 'Increase Google Ads Budget',
    description: 'Your Google Ads campaigns are performing exceptionally well with a 4.2x ROAS. Consider increasing budget by 30% to capture more conversions.',
    impact: 'high',
    metric: 'Potential Revenue Increase',
    value: '₹2,85,000',
    change: '+23%'
  },
  {
    id: '2',
    type: 'warning',
    title: 'Cart Abandonment Rate Rising',
    description: 'Cart abandonment rate has increased to 72% this week, up from 68% last week. Consider implementing exit-intent popups or email reminders.',
    impact: 'high',
    metric: 'Lost Revenue',
    value: '₹4,20,000',
    change: '+6%'
  },
  {
    id: '3',
    type: 'trend',
    title: 'Mobile Traffic Surge',
    description: 'Mobile traffic has increased by 45% this month. Ensure your mobile checkout experience is optimized for better conversions.',
    impact: 'medium',
    metric: 'Mobile Conversion Rate',
    value: '2.8%',
    change: '+0.5%'
  },
  {
    id: '4',
    type: 'recommendation',
    title: 'Optimize Product Descriptions',
    description: 'Products with detailed descriptions have 35% higher conversion rates. Consider enhancing descriptions for your top 20 products.',
    impact: 'medium',
    metric: 'Conversion Rate Improvement',
    value: '1.2%',
    change: '+35%'
  }
]

export default function AIAssistantPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Hello! I\'m your D2C Analytics AI Assistant. I can help you analyze your data, identify opportunities, and provide actionable insights. What would you like to know about your business performance?',
      timestamp: new Date(),
      suggestions: [
        'Show me my top performing products',
        'What\'s my customer acquisition cost?',
        'Analyze my marketing ROI',
        'Identify growth opportunities'
      ]
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: generateAIResponse(inputMessage),
        timestamp: new Date(),
        suggestions: [
          'Tell me more about this',
          'Show me the data',
          'What should I do next?',
          'Compare with last month'
        ]
      }
      setMessages(prev => [...prev, aiResponse])
      setIsLoading(false)
    }, 1500)
  }

  const generateAIResponse = (query: string): string => {
    const responses = {
      'top performing products': 'Based on your data, your top 3 performing products are:\n\n1. **Premium T-Shirts** - ₹28,50,000 revenue (65% margin)\n2. **Wireless Headphones** - ₹19,20,000 revenue (45% margin)\n3. **Smart Watches** - ₹16,80,000 revenue (55% margin)\n\nThe Premium T-Shirts are your clear winner with the highest revenue and margin. Consider expanding this product line or creating similar variations.',
      'customer acquisition cost': 'Your current Customer Acquisition Cost (CAC) is ₹245 across all channels:\n\n• **Google Ads**: ₹162 CAC\n• **Facebook Ads**: ₹189 CAC\n• **Instagram Ads**: ₹249 CAC\n\nYour Google Ads have the most efficient CAC. With a Customer Lifetime Value of ₹4,580, you have a healthy 18.7:1 LTV:CAC ratio.',
      'marketing roi': 'Your marketing ROI analysis shows:\n\n• **Overall ROAS**: 4.2x\n• **Google Ads**: 4.2x ROAS (₹1,25,000 spend)\n• **Facebook Ads**: 3.8x ROAS (₹98,000 spend)\n• **Instagram Ads**: 3.5x ROAS (₹75,000 spend)\n\nAll channels are performing above the 3x benchmark. Consider reallocating budget from Instagram to Google Ads for better returns.',
      'growth opportunities': 'I\'ve identified several growth opportunities:\n\n1. **Increase Google Ads budget** - High ROAS potential\n2. **Reduce cart abandonment** - 72% rate is costing you ₹4.2L monthly\n3. **Expand to Tier 2 cities** - 40% lower CAC, growing market\n4. **Launch email marketing** - 25% of customers haven\'t received any emails\n5. **Optimize mobile experience** - 45% traffic increase needs better conversion'
    }

    const lowerQuery = query.toLowerCase()
    for (const [key, response] of Object.entries(responses)) {
      if (lowerQuery.includes(key)) {
        return response
      }
    }

    return 'I can help you analyze various aspects of your D2C business including sales performance, marketing ROI, customer behavior, and growth opportunities. Could you be more specific about what you\'d like to know?'
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInputMessage(suggestion)
  }

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'opportunity': return <TrendingUp className="h-5 w-5 text-green-600" />
      case 'warning': return <AlertTriangle className="h-5 w-5 text-red-600" />
      case 'trend': return <BarChart3 className="h-5 w-5 text-blue-600" />
      case 'recommendation': return <Lightbulb className="h-5 w-5 text-yellow-600" />
      default: return <Sparkles className="h-5 w-5 text-purple-600" />
    }
  }

  const getInsightColor = (type: string) => {
    switch (type) {
      case 'opportunity': return 'border-green-200 bg-green-50'
      case 'warning': return 'border-red-200 bg-red-50'
      case 'trend': return 'border-blue-200 bg-blue-50'
      case 'recommendation': return 'border-yellow-200 bg-yellow-50'
      default: return 'border-purple-200 bg-purple-50'
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Brain className="h-8 w-8 mr-3 text-purple-600" />
            AI Analytics Assistant
          </h1>
          <p className="text-gray-600 mt-2">
            Get intelligent insights and recommendations powered by AI
          </p>
        </div>
        <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-200">
          <Sparkles className="h-4 w-4 mr-1" />
          AI Powered
        </Badge>
      </div>

      <Tabs defaultValue="chat" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="chat" className="flex items-center">
            <MessageSquare className="h-4 w-4 mr-2" />
            AI Chat
          </TabsTrigger>
          <TabsTrigger value="insights" className="flex items-center">
            <Lightbulb className="h-4 w-4 mr-2" />
            Smart Insights
          </TabsTrigger>
          <TabsTrigger value="recommendations" className="flex items-center">
            <Target className="h-4 w-4 mr-2" />
            Recommendations
          </TabsTrigger>
        </TabsList>

        {/* AI Chat Tab */}
        <TabsContent value="chat">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <Card className="lg:col-span-3">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Bot className="h-5 w-5 mr-2 text-purple-600" />
                  AI Assistant Chat
                </CardTitle>
                <CardDescription>
                  Ask questions about your business data and get intelligent insights
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ScrollArea className="h-[500px] pr-4">
                  <div className="space-y-4">
                    {messages.map((message) => (
                      <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-lg p-4 ${
                          message.type === 'user' 
                            ? 'bg-blue-600 text-white' 
                            : 'bg-gray-100 text-gray-900'
                        }`}>
                          <div className="flex items-start space-x-2">
                            {message.type === 'assistant' && <Bot className="h-5 w-5 mt-0.5 text-purple-600" />}
                            {message.type === 'user' && <User className="h-5 w-5 mt-0.5" />}
                            <div className="flex-1">
                              <div className="whitespace-pre-wrap">{message.content}</div>
                              {message.suggestions && (
                                <div className="mt-3 space-y-2">
                                  <div className="text-sm opacity-75">Suggested questions:</div>
                                  <div className="flex flex-wrap gap-2">
                                    {message.suggestions.map((suggestion, index) => (
                                      <Button
                                        key={index}
                                        variant="outline"
                                        size="sm"
                                        className="text-xs"
                                        onClick={() => handleSuggestionClick(suggestion)}
                                      >
                                        {suggestion}
                                      </Button>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                    {isLoading && (
                      <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-lg p-4 max-w-[80%]">
                          <div className="flex items-center space-x-2">
                            <Bot className="h-5 w-5 text-purple-600" />
                            <div className="flex space-x-1">
                              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </ScrollArea>
                
                <div className="flex space-x-2">
                  <Input
                    placeholder="Ask me anything about your business data..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    disabled={isLoading}
                  />
                  <Button onClick={sendMessage} disabled={isLoading || !inputMessage.trim()}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => handleSuggestionClick('Show me my top performing products')}
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Top Products
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => handleSuggestionClick('What\'s my customer acquisition cost?')}
                >
                  <Users className="h-4 w-4 mr-2" />
                  Customer CAC
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => handleSuggestionClick('Analyze my marketing ROI')}
                >
                  <Target className="h-4 w-4 mr-2" />
                  Marketing ROI
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => handleSuggestionClick('Identify growth opportunities')}
                >
                  <TrendingUp className="h-4 w-4 mr-2" />
                  Growth Opportunities
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Smart Insights Tab */}
        <TabsContent value="insights">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {aiInsights.map((insight) => (
              <Card key={insight.id} className={`border-2 ${getInsightColor(insight.type)}`}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center">
                      {getInsightIcon(insight.type)}
                      <span className="ml-2">{insight.title}</span>
                    </div>
                    <Badge variant={insight.impact === 'high' ? 'destructive' : insight.impact === 'medium' ? 'default' : 'secondary'}>
                      {insight.impact} impact
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 mb-4">{insight.description}</p>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm text-gray-600">{insight.metric}</div>
                      <div className="text-lg font-bold">{insight.value}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-600">Change</div>
                      <div className="text-lg font-bold text-green-600">{insight.change}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Recommendations Tab */}
        <TabsContent value="recommendations">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="h-5 w-5 mr-2 text-yellow-600" />
                  Priority Actions
                </CardTitle>
                <CardDescription>
                  AI-recommended actions to improve your business performance
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      title: 'Optimize Google Ads Budget Allocation',
                      description: 'Increase budget by 30% for high-performing campaigns',
                      impact: '₹2,85,000 potential revenue increase',
                      priority: 'High',
                      effort: 'Low'
                    },
                    {
                      title: 'Implement Cart Abandonment Recovery',
                      description: 'Set up email sequences for abandoned carts',
                      impact: '₹4,20,000 recovered revenue monthly',
                      priority: 'High',
                      effort: 'Medium'
                    },
                    {
                      title: 'Expand to Tier 2 Cities',
                      description: 'Launch targeted campaigns in emerging markets',
                      impact: '40% lower CAC, 25% market expansion',
                      priority: 'Medium',
                      effort: 'High'
                    },
                    {
                      title: 'Enhance Mobile Experience',
                      description: 'Optimize checkout flow for mobile users',
                      impact: '1.2% conversion rate improvement',
                      priority: 'Medium',
                      effort: 'Medium'
                    }
                  ].map((rec, index) => (
                    <div key={index} className="border rounded-lg p-4 hover:bg-gray-50">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-900">{rec.title}</h4>
                          <p className="text-gray-600 mt-1">{rec.description}</p>
                          <p className="text-green-600 font-medium mt-2">{rec.impact}</p>
                        </div>
                        <div className="flex flex-col items-end space-y-2">
                          <Badge variant={rec.priority === 'High' ? 'destructive' : 'default'}>
                            {rec.priority} Priority
                          </Badge>
                          <Badge variant="outline">
                            {rec.effort} Effort
                          </Badge>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}