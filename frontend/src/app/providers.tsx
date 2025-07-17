"use client"

import type React from "react"

import { QueryClient, QueryClientProvider } from "react-query"
import { Toaster } from "react-hot-toast"
import { useState } from "react"

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster position="top-right" />
    </QueryClientProvider>
  )
}
