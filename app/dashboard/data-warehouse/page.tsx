'use client'

import { DataWarehousePanel } from '@/components/dashboard/data-warehouse-panel'

export default function DataWarehousePage() {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Data Warehouse</h1>
        <p className="text-gray-600 mt-2">
          Manage your BigQuery data warehouse, upload data, run queries, and export results
        </p>
      </div>
      <DataWarehousePanel />
    </div>
  )
}