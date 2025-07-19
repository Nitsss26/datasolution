'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  BarChart3,
  Database,
  ShoppingBag,
  Target,
  Truck,
  Users,
  DollarSign,
  TrendingUp,
  Settings,
  Upload,
  Download,
  RefreshCw,
  ChevronDown,
  ChevronRight,
  Home,
  Table,
  PieChart,
  LineChart,
  Activity,
  FileText,
  Zap,
  Globe,
  Package,
  CreditCard,
  MessageSquare,
  Bell,
  HelpCircle,
  LogOut,
  ChevronLeft,
  Menu
} from 'lucide-react'

interface SidebarProps {
  className?: string
}

interface NavItem {
  title: string
  href?: string
  icon: any
  badge?: string
  children?: NavItem[]
  isExpanded?: boolean
}

const navigationItems: NavItem[] = [
  {
    title: 'Dashboard',
    href: '/dashboard',
    icon: Home,
  },
  {
    title: 'Data Warehouse',
    icon: Database,
    badge: 'BigQuery',
    children: [
      { title: 'Data Sources', href: '/dashboard/data-sources', icon: Globe },
      { title: 'Upload Data', href: '/dashboard/upload', icon: Upload },
      { title: 'Query Builder', href: '/dashboard/query', icon: Database },
      { title: 'Data Export', href: '/dashboard/export', icon: Download },
      { title: 'Schema Manager', href: '/dashboard/schema', icon: Table },
    ]
  },
  {
    title: 'Connectors',
    icon: Zap,
    children: [
      { title: 'Shopify', href: '/dashboard/connectors/shopify', icon: ShoppingBag, badge: 'Connected' },
      { title: 'Shiprocket', href: '/dashboard/connectors/shiprocket', icon: Truck, badge: 'Connected' },
      { title: 'Google Ads', href: '/dashboard/connectors/google-ads', icon: Target, badge: 'Connected' },
      { title: 'Meta Ads', href: '/dashboard/connectors/meta-ads', icon: Target, badge: 'Connected' },
      { title: 'Amazon', href: '/dashboard/connectors/amazon', icon: Package, badge: 'Coming Soon' },
      { title: 'Zepto', href: '/dashboard/connectors/zepto', icon: Zap, badge: 'Coming Soon' },
      { title: 'Blinkit', href: '/dashboard/connectors/blinkit', icon: Zap, badge: 'Coming Soon' },
    ]
  },
  {
    title: 'Analytics',
    icon: BarChart3,
    children: [
      { title: 'Revenue Analytics', href: '/dashboard/analytics/revenue', icon: DollarSign },
      { title: 'Sales Performance', href: '/dashboard/analytics/sales', icon: TrendingUp },
      { title: 'Customer Analytics', href: '/dashboard/analytics/customers', icon: Users },
      { title: 'Marketing ROI', href: '/dashboard/analytics/marketing', icon: Target },
      { title: 'Operations', href: '/dashboard/analytics/operations', icon: Truck },
      { title: 'P&L Reports', href: '/dashboard/analytics/pl', icon: FileText },
    ]
  },
  {
    title: 'Data Tables',
    href: '/dashboard/tables',
    icon: Table,
  },
  {
    title: 'Charts & Visualizations',
    icon: PieChart,
    children: [
      { title: 'Chart Builder', href: '/dashboard/charts/builder', icon: BarChart3 },
      { title: 'Custom Dashboards', href: '/dashboard/charts/custom', icon: PieChart },
      { title: 'Report Templates', href: '/dashboard/charts/templates', icon: FileText },
      { title: 'Data Stories', href: '/dashboard/charts/stories', icon: MessageSquare },
    ]
  },
  {
    title: 'AI Assistant',
    href: '/dashboard/ai',
    icon: MessageSquare,
    badge: 'New',
  },
]

const bottomNavItems: NavItem[] = [
  { title: 'Settings', href: '/dashboard/settings', icon: Settings },
  { title: 'Help & Support', href: '/dashboard/help', icon: HelpCircle },
  { title: 'Notifications', href: '/dashboard/notifications', icon: Bell },
]

export function Sidebar({ className }: SidebarProps) {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = useState(false)
  const [expandedItems, setExpandedItems] = useState<string[]>(['Connectors', 'Analytics'])

  const toggleExpanded = (title: string) => {
    setExpandedItems(prev => 
      prev.includes(title) 
        ? prev.filter(item => item !== title)
        : [...prev, title]
    )
  }

  const renderNavItem = (item: NavItem, level = 0) => {
    const isActive = pathname === item.href
    const isExpanded = expandedItems.includes(item.title)
    const hasChildren = item.children && item.children.length > 0

    return (
      <div key={item.title}>
        {item.href ? (
          <Link href={item.href}>
            <Button
              variant={isActive ? "secondary" : "ghost"}
              className={cn(
                "w-full justify-start h-10 px-3",
                level > 0 && "ml-4 w-[calc(100%-1rem)]",
                isActive && "bg-blue-100 text-blue-700 border-r-2 border-blue-600",
                collapsed && level === 0 && "px-2"
              )}
            >
              <item.icon className={cn("h-4 w-4", !collapsed && "mr-3")} />
              {!collapsed && (
                <>
                  <span className="flex-1 text-left">{item.title}</span>
                  {item.badge && (
                    <Badge 
                      variant={item.badge === 'Connected' ? 'default' : 'secondary'} 
                      className="ml-2 text-xs"
                    >
                      {item.badge}
                    </Badge>
                  )}
                </>
              )}
            </Button>
          </Link>
        ) : (
          <Button
            variant="ghost"
            className={cn(
              "w-full justify-start h-10 px-3",
              level > 0 && "ml-4 w-[calc(100%-1rem)]",
              collapsed && level === 0 && "px-2"
            )}
            onClick={() => !collapsed && hasChildren && toggleExpanded(item.title)}
          >
            <item.icon className={cn("h-4 w-4", !collapsed && "mr-3")} />
            {!collapsed && (
              <>
                <span className="flex-1 text-left">{item.title}</span>
                {item.badge && (
                  <Badge variant="outline" className="ml-2 text-xs">
                    {item.badge}
                  </Badge>
                )}
                {hasChildren && (
                  isExpanded ? 
                    <ChevronDown className="h-4 w-4 ml-2" /> : 
                    <ChevronRight className="h-4 w-4 ml-2" />
                )}
              </>
            )}
          </Button>
        )}
        
        {!collapsed && hasChildren && isExpanded && (
          <div className="mt-1 space-y-1">
            {item.children?.map(child => renderNavItem(child, level + 1))}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className={cn(
      "flex flex-col h-full bg-white border-r border-gray-200 transition-all duration-300",
      collapsed ? "w-16" : "w-64",
      className
    )}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        {!collapsed && (
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-6 w-6 text-blue-600" />
            <span className="font-bold text-lg">D2C Analytics</span>
          </div>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setCollapsed(!collapsed)}
          className="h-8 w-8 p-0"
        >
          {collapsed ? <Menu className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>

      {/* Navigation */}
      <ScrollArea className="flex-1 px-3 py-4">
        <div className="space-y-2">
          {navigationItems.map(item => renderNavItem(item))}
        </div>
      </ScrollArea>

      {/* Bottom Navigation */}
      <div className="border-t p-3">
        <div className="space-y-1">
          {bottomNavItems.map(item => renderNavItem(item))}
        </div>
        <Separator className="my-3" />
        <Button
          variant="ghost"
          className={cn(
            "w-full justify-start h-10 px-3 text-red-600 hover:text-red-700 hover:bg-red-50",
            collapsed && "px-2"
          )}
        >
          <LogOut className={cn("h-4 w-4", !collapsed && "mr-3")} />
          {!collapsed && "Sign Out"}
        </Button>
      </div>
    </div>
  )
}