'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Slider } from '@/components/ui/slider'
import { Switch } from '@/components/ui/switch'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { 
  Palette, 
  Monitor, 
  Sun, 
  Moon, 
  Smartphone,
  X,
  RotateCcw,
  Check
} from 'lucide-react'
import { useTheme } from 'next-themes'

interface ThemeCustomizerProps {
  onClose: () => void
}

const COLOR_SCHEMES = [
  { name: 'Blue', value: 'blue', colors: ['#3b82f6', '#1d4ed8', '#1e40af'] },
  { name: 'Green', value: 'green', colors: ['#10b981', '#059669', '#047857'] },
  { name: 'Purple', value: 'purple', colors: ['#8b5cf6', '#7c3aed', '#6d28d9'] },
  { name: 'Orange', value: 'orange', colors: ['#f59e0b', '#d97706', '#b45309'] },
  { name: 'Red', value: 'red', colors: ['#ef4444', '#dc2626', '#b91c1c'] },
  { name: 'Pink', value: 'pink', colors: ['#ec4899', '#db2777', '#be185d'] },
  { name: 'Indigo', value: 'indigo', colors: ['#6366f1', '#4f46e5', '#4338ca'] },
  { name: 'Teal', value: 'teal', colors: ['#14b8a6', '#0d9488', '#0f766e'] }
]

const FONT_FAMILIES = [
  { name: 'Inter', value: 'Inter, sans-serif' },
  { name: 'Roboto', value: 'Roboto, sans-serif' },
  { name: 'Open Sans', value: 'Open Sans, sans-serif' },
  { name: 'Poppins', value: 'Poppins, sans-serif' },
  { name: 'Lato', value: 'Lato, sans-serif' },
  { name: 'Montserrat', value: 'Montserrat, sans-serif' }
]

export function ThemeCustomizer({ onClose }: ThemeCustomizerProps) {
  const { theme, setTheme } = useTheme()
  const [colorScheme, setColorScheme] = useState('blue')
  const [fontSize, setFontSize] = useState([14])
  const [fontFamily, setFontFamily] = useState('Inter, sans-serif')
  const [compactMode, setCompactMode] = useState(false)
  const [animations, setAnimations] = useState(true)
  const [borderRadius, setBorderRadius] = useState([8])
  const [hasChanges, setHasChanges] = useState(false)

  const handleColorSchemeChange = (scheme: string) => {
    setColorScheme(scheme)
    setHasChanges(true)
    
    // Apply color scheme to CSS variables
    const selectedScheme = COLOR_SCHEMES.find(s => s.value === scheme)
    if (selectedScheme) {
      document.documentElement.style.setProperty('--primary', selectedScheme.colors[0])
      document.documentElement.style.setProperty('--primary-dark', selectedScheme.colors[1])
      document.documentElement.style.setProperty('--primary-darker', selectedScheme.colors[2])
    }
  }

  const handleFontSizeChange = (value: number[]) => {
    setFontSize(value)
    setHasChanges(true)
    document.documentElement.style.setProperty('--font-size-base', `${value[0]}px`)
  }

  const handleFontFamilyChange = (family: string) => {
    setFontFamily(family)
    setHasChanges(true)
    document.documentElement.style.setProperty('--font-family', family)
  }

  const handleBorderRadiusChange = (value: number[]) => {
    setBorderRadius(value)
    setHasChanges(true)
    document.documentElement.style.setProperty('--radius', `${value[0]}px`)
  }

  const handleCompactModeChange = (enabled: boolean) => {
    setCompactMode(enabled)
    setHasChanges(true)
    document.documentElement.classList.toggle('compact-mode', enabled)
  }

  const handleAnimationsChange = (enabled: boolean) => {
    setAnimations(enabled)
    setHasChanges(true)
    document.documentElement.classList.toggle('no-animations', !enabled)
  }

  const handleReset = () => {
    setColorScheme('blue')
    setFontSize([14])
    setFontFamily('Inter, sans-serif')
    setCompactMode(false)
    setAnimations(true)
    setBorderRadius([8])
    setHasChanges(false)
    
    // Reset CSS variables
    document.documentElement.style.removeProperty('--primary')
    document.documentElement.style.removeProperty('--primary-dark')
    document.documentElement.style.removeProperty('--primary-darker')
    document.documentElement.style.removeProperty('--font-size-base')
    document.documentElement.style.removeProperty('--font-family')
    document.documentElement.style.removeProperty('--radius')
    document.documentElement.classList.remove('compact-mode', 'no-animations')
  }

  const handleApply = () => {
    setHasChanges(false)
    // In a real app, you would save these preferences to localStorage or user settings
    localStorage.setItem('theme-preferences', JSON.stringify({
      colorScheme,
      fontSize: fontSize[0],
      fontFamily,
      compactMode,
      animations,
      borderRadius: borderRadius[0]
    }))
  }

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
        <div className="flex items-center gap-2">
          <Palette className="h-5 w-5 text-primary" />
          <CardTitle>Theme Customizer</CardTitle>
          {hasChanges && (
            <Badge variant="outline" className="text-orange-600 border-orange-600">
              Unsaved Changes
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleReset}>
            <RotateCcw className="h-4 w-4 mr-2" />
            Reset
          </Button>
          <Button size="sm" onClick={handleApply} disabled={!hasChanges}>
            <Check className="h-4 w-4 mr-2" />
            Apply
          </Button>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Theme Mode */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Theme Mode</Label>
            <div className="grid grid-cols-3 gap-2">
              <Button
                variant={theme === 'light' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setTheme('light')}
                className="flex flex-col items-center gap-1 h-auto py-3"
              >
                <Sun className="h-4 w-4" />
                <span className="text-xs">Light</span>
              </Button>
              <Button
                variant={theme === 'dark' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setTheme('dark')}
                className="flex flex-col items-center gap-1 h-auto py-3"
              >
                <Moon className="h-4 w-4" />
                <span className="text-xs">Dark</span>
              </Button>
              <Button
                variant={theme === 'system' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setTheme('system')}
                className="flex flex-col items-center gap-1 h-auto py-3"
              >
                <Monitor className="h-4 w-4" />
                <span className="text-xs">System</span>
              </Button>
            </div>
          </div>

          {/* Color Scheme */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Color Scheme</Label>
            <div className="grid grid-cols-4 gap-2">
              {COLOR_SCHEMES.map((scheme) => (
                <Button
                  key={scheme.value}
                  variant={colorScheme === scheme.value ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => handleColorSchemeChange(scheme.value)}
                  className="flex flex-col items-center gap-1 h-auto py-2"
                >
                  <div className="flex gap-1">
                    {scheme.colors.map((color, index) => (
                      <div
                        key={index}
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                  <span className="text-xs">{scheme.name}</span>
                </Button>
              ))}
            </div>
          </div>

          {/* Font Family */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Font Family</Label>
            <Select value={fontFamily} onValueChange={handleFontFamilyChange}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {FONT_FAMILIES.map((font) => (
                  <SelectItem key={font.value} value={font.value}>
                    <span style={{ fontFamily: font.value }}>{font.name}</span>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <Separator />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Font Size */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-sm font-medium">Font Size</Label>
              <Badge variant="outline">{fontSize[0]}px</Badge>
            </div>
            <Slider
              value={fontSize}
              onValueChange={handleFontSizeChange}
              max={20}
              min={12}
              step={1}
              className="w-full"
            />
          </div>

          {/* Border Radius */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label className="text-sm font-medium">Border Radius</Label>
              <Badge variant="outline">{borderRadius[0]}px</Badge>
            </div>
            <Slider
              value={borderRadius}
              onValueChange={handleBorderRadiusChange}
              max={20}
              min={0}
              step={1}
              className="w-full"
            />
          </div>
        </div>

        <Separator />

        {/* Toggle Options */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label className="text-sm font-medium">Compact Mode</Label>
              <p className="text-xs text-muted-foreground">
                Reduce spacing and padding for denser layouts
              </p>
            </div>
            <Switch
              checked={compactMode}
              onCheckedChange={handleCompactModeChange}
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <Label className="text-sm font-medium">Animations</Label>
              <p className="text-xs text-muted-foreground">
                Enable smooth transitions and animations
              </p>
            </div>
            <Switch
              checked={animations}
              onCheckedChange={handleAnimationsChange}
            />
          </div>
        </div>

        <Separator />

        {/* Preview */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Preview</Label>
          <div className="p-4 border rounded-lg bg-card">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold">Sample Dashboard Card</h3>
                <Badge>Preview</Badge>
              </div>
              <p className="text-sm text-muted-foreground">
                This is how your dashboard will look with the current theme settings.
              </p>
              <div className="flex gap-2">
                <Button size="sm">Primary Button</Button>
                <Button variant="outline" size="sm">Secondary Button</Button>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}