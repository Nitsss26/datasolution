'use client'

import { useState, useRef, useEffect } from 'react'
import { AppHeader } from '@/components/navigation'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Loader2, Send } from 'lucide-react'
import { useAI, Message } from '@/hooks/use-ai'

export default function AIAssistantPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { askAI } = useAI()
  
  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!input.trim() || loading) return
    
    const userMessage = { role: 'user', content: input } as Message
    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    setInput('')
    
    try {
      const response = await askAI(input)
      
      const assistantMessage = {
        role: 'assistant',
        content: response.error ? 
          "I'm sorry, I encountered an error processing your request. Please try again later." : 
          response.response
      } as Message
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error in AI chat:', error)
      
      const errorMessage = {
        role: 'assistant',
        content: "I'm sorry, I encountered an error. Please try again later."
      } as Message
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="min-h-screen bg-background">
      <AppHeader />
      
      <div className="container mx-auto p-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-6">AI Assistant</h1>
          
          <Card className="w-full">
            <CardHeader>
              <CardTitle>Ask me anything about your data</CardTitle>
              <CardDescription>
                I can help you analyze your data, generate insights, and answer questions about your business performance.
              </CardDescription>
            </CardHeader>
            
            <CardContent className="h-[500px] flex flex-col">
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                  <div className="text-center text-muted-foreground py-8">
                    No messages yet. Start by asking a question below.
                  </div>
                ) : (
                  messages.map((message, index) => (
                    <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div
                        className={`max-w-[80%] rounded-lg px-4 py-2 ${
                          message.role === 'user'
                            ? 'bg-primary text-primary-foreground'
                            : 'bg-muted text-foreground'
                        }`}
                      >
                        {message.content}
                      </div>
                    </div>
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>
            </CardContent>
            
            <CardFooter>
              <form onSubmit={handleSubmit} className="flex gap-2 w-full">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask a question about your data..."
                  className="flex-1"
                  disabled={loading}
                />
                <Button type="submit" disabled={loading || !input.trim()}>
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
              </form>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  )
}