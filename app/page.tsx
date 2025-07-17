"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { BarChart3, TrendingUp, Users, ShoppingCart, DollarSign, Target } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  const [email, setEmail] = useState("")

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-900">D2C Analytics</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">All-in-One D2C Data Solution</h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Connect all your platforms - Shopify, Amazon, Facebook Ads, Google Ads, and more. Get unified analytics,
            beautiful dashboards, and actionable insights to grow your D2C business.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/register">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3">
                Start Free Trial
              </Button>
            </Link>
            <Link href="/demo">
              <Button size="lg" variant="outline" className="px-8 py-3 bg-transparent">
                View Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Everything You Need to Scale Your D2C Business
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <TrendingUp className="h-12 w-12 text-blue-600 mb-4" />
                <CardTitle>Unified Analytics</CardTitle>
                <CardDescription>
                  Connect all your platforms and get a single view of your business performance
                </CardDescription>
              </CardHeader>
            </Card>
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <Target className="h-12 w-12 text-green-600 mb-4" />
                <CardTitle>Smart Insights</CardTitle>
                <CardDescription>
                  AI-powered recommendations to optimize your marketing spend and increase ROI
                </CardDescription>
              </CardHeader>
            </Card>
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <BarChart3 className="h-12 w-12 text-purple-600 mb-4" />
                <CardTitle>Beautiful Dashboards</CardTitle>
                <CardDescription>
                  Stunning visualizations that make complex data easy to understand and act upon
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Integrations Section */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Connect All Your Platforms</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { name: "Shopify", logo: "🛍️" },
              { name: "Amazon", logo: "📦" },
              { name: "Facebook Ads", logo: "📘" },
              { name: "Google Ads", logo: "🎯" },
              { name: "Flipkart", logo: "🛒" },
              { name: "Shiprocket", logo: "🚚" },
              { name: "Zepto", logo: "⚡" },
              { name: "Blinkit", logo: "🏃" },
            ].map((platform) => (
              <Card key={platform.name} className="text-center p-6 hover:shadow-lg transition-shadow">
                <div className="text-4xl mb-2">{platform.logo}</div>
                <h3 className="font-semibold">{platform.name}</h3>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Metrics Preview */}
      <section className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Track What Matters Most</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <Card className="text-center p-6">
              <DollarSign className="h-8 w-8 text-green-600 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-gray-900">₹2.5M+</h3>
              <p className="text-gray-600">Total Revenue</p>
            </Card>
            <Card className="text-center p-6">
              <ShoppingCart className="h-8 w-8 text-blue-600 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-gray-900">15,000+</h3>
              <p className="text-gray-600">Orders Processed</p>
            </Card>
            <Card className="text-center p-6">
              <Target className="h-8 w-8 text-purple-600 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-gray-900">4.2x</h3>
              <p className="text-gray-600">Average ROAS</p>
            </Card>
            <Card className="text-center p-6">
              <Users className="h-8 w-8 text-orange-600 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-gray-900">8,500+</h3>
              <p className="text-gray-600">Active Customers</p>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Scale Your D2C Business?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of D2C brands using our platform to make data-driven decisions
          </p>
          <div className="max-w-md mx-auto flex gap-4">
            <Input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-white text-gray-900"
            />
            <Button className="bg-white text-blue-600 hover:bg-gray-100">Get Started</Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <BarChart3 className="h-6 w-6" />
                <span className="text-xl font-bold">D2C Analytics</span>
              </div>
              <p className="text-gray-400">The complete data solution for D2C brands</p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="/features">Features</Link>
                </li>
                <li>
                  <Link href="/integrations">Integrations</Link>
                </li>
                <li>
                  <Link href="/pricing">Pricing</Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="/about">About</Link>
                </li>
                <li>
                  <Link href="/contact">Contact</Link>
                </li>
                <li>
                  <Link href="/blog">Blog</Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="/help">Help Center</Link>
                </li>
                <li>
                  <Link href="/docs">Documentation</Link>
                </li>
                <li>
                  <Link href="/api">API</Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 D2C Analytics. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
