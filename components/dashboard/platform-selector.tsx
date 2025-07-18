'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { ChevronDown, Check, Circle } from 'lucide-react'

interface Platform {
  id: string
  name: string
  connected: boolean
  lastSync?: string
  dataPoints?: number
}

interface PlatformSelectorProps {
  platforms: Platform[]
  selected: string[]
  onChange: (selected: string[]) => void
}

export function PlatformSelector({ platforms, selected, onChange }: PlatformSelectorProps) {
  const [open, setOpen] = useState(false)

  const handleSelectAll = () => {
    if (selected.includes('all')) {
      onChange([])
    } else {
      onChange(['all'])
    }
  }

  const handleSelectPlatform = (platformId: string) => {
    if (selected.includes('all')) {
      // If "all" is selected, deselect it and select only this platform
      onChange([platformId])
    } else if (selected.includes(platformId)) {
      // Remove this platform
      const newSelected = selected.filter(id => id !== platformId)
      onChange(newSelected)
    } else {
      // Add this platform
      onChange([...selected, platformId])
    }
  }

  const getSelectedText = () => {
    if (selected.includes('all')) {
      return 'All Platforms'
    }
    if (selected.length === 0) {
      return 'Select platforms'
    }
    if (selected.length === 1) {
      const platform = platforms.find(p => p.id === selected[0])
      return platform?.name || 'Unknown'
    }
    return `${selected.length} platforms selected`
  }

  const connectedPlatforms = platforms.filter(p => p.connected)
  const disconnectedPlatforms = platforms.filter(p => !p.connected)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between"
        >
          {getSelectedText()}
          <ChevronDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0" align="start">
        <Card className="border-0 shadow-none">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Select Data Sources</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* All Platforms Option */}
            <div className="flex items-center space-x-2">
              <Checkbox
                id="all"
                checked={selected.includes('all')}
                onCheckedChange={handleSelectAll}
              />
              <Label htmlFor="all" className="text-sm font-medium">
                All Platforms
              </Label>
              <Badge variant="outline" className="ml-auto">
                {connectedPlatforms.length} connected
              </Badge>
            </div>

            {/* Connected Platforms */}
            {connectedPlatforms.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                  Connected Platforms
                </h4>
                {connectedPlatforms.map((platform) => (
                  <div key={platform.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={platform.id}
                      checked={selected.includes('all') || selected.includes(platform.id)}
                      onCheckedChange={() => handleSelectPlatform(platform.id)}
                      disabled={selected.includes('all')}
                    />
                    <div className="flex items-center space-x-2 flex-1">
                      <Circle className="h-2 w-2 fill-green-500 text-green-500" />
                      <Label htmlFor={platform.id} className="text-sm flex-1">
                        {platform.name}
                      </Label>
                      <div className="text-xs text-muted-foreground">
                        {platform.dataPoints?.toLocaleString()} records
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Disconnected Platforms */}
            {disconnectedPlatforms.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                  Available Platforms
                </h4>
                {disconnectedPlatforms.map((platform) => (
                  <div key={platform.id} className="flex items-center space-x-2 opacity-50">
                    <Checkbox
                      id={platform.id}
                      disabled
                      checked={false}
                    />
                    <div className="flex items-center space-x-2 flex-1">
                      <Circle className="h-2 w-2 fill-gray-400 text-gray-400" />
                      <Label htmlFor={platform.id} className="text-sm flex-1">
                        {platform.name}
                      </Label>
                      <Badge variant="secondary" className="text-xs">
                        Not connected
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Summary */}
            <div className="pt-2 border-t">
              <div className="text-xs text-muted-foreground">
                {selected.includes('all') 
                  ? `Analyzing data from all ${connectedPlatforms.length} connected platforms`
                  : selected.length === 0
                  ? 'No platforms selected'
                  : `Analyzing data from ${selected.length} selected platform${selected.length > 1 ? 's' : ''}`
                }
              </div>
            </div>
          </CardContent>
        </Card>
      </PopoverContent>
    </Popover>
  )
}