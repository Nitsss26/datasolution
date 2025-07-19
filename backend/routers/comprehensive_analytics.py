from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import asyncio

from ..database import get_database
from ..utils.bigquery_client import BigQueryClient
from ..utils.data_processor import DataProcessor

router = APIRouter()

class ComprehensiveAnalyticsRequest(BaseModel):
    platforms: List[str] = ["all"]
    time_range: str = "30d"
    metrics: Optional[List[str]] = None
    granularity: str = "daily"
    filters: Optional[Dict[str, Any]] = None

class DataExportRequest(BaseModel):
    format: str = "csv"
    platforms: List[str] = ["all"]
    time_range: str = "30d"
    tables: Optional[List[str]] = None

@router.get("/comprehensive-data")
async def get_comprehensive_data(
    platforms: str = Query("all", description="Comma-separated list of platforms"),
    time_range: str = Query("30d", description="Time range for data"),
    include_raw: bool = Query(False, description="Include raw data tables")
):
    """Get comprehensive data from all connected platforms"""
    try:
        platform_list = platforms.split(",") if platforms != "all" else ["all"]
        
        # Sample comprehensive data structure
        comprehensive_data = {
            "shopify": {
                "orders": await get_shopify_orders_data(time_range),
                "customers": await get_shopify_customers_data(time_range),
                "products": await get_shopify_products_data(time_range),
                "inventory": await get_shopify_inventory_data(),
                "transactions": await get_shopify_transactions_data(time_range),
                "analytics": await get_shopify_analytics_data(time_range)
            },
            "google_ads": {
                "campaigns": await get_google_ads_campaigns_data(time_range),
                "ad_groups": await get_google_ads_adgroups_data(time_range),
                "keywords": await get_google_ads_keywords_data(time_range),
                "ads": await get_google_ads_ads_data(time_range),
                "performance": await get_google_ads_performance_data(time_range),
                "demographics": await get_google_ads_demographics_data(time_range)
            },
            "meta_ads": {
                "campaigns": await get_meta_ads_campaigns_data(time_range),
                "ad_sets": await get_meta_ads_adsets_data(time_range),
                "ads": await get_meta_ads_ads_data(time_range),
                "insights": await get_meta_ads_insights_data(time_range),
                "audiences": await get_meta_ads_audiences_data(time_range),
                "creatives": await get_meta_ads_creatives_data(time_range)
            },
            "shiprocket": {
                "shipments": await get_shiprocket_shipments_data(time_range),
                "tracking": await get_shiprocket_tracking_data(time_range),
                "returns": await get_shiprocket_returns_data(time_range),
                "couriers": await get_shiprocket_couriers_data(),
                "zones": await get_shiprocket_zones_data(),
                "performance": await get_shiprocket_performance_data(time_range)
            }
        }
        
        # Filter by requested platforms
        if platform_list != ["all"]:
            comprehensive_data = {
                platform: data for platform, data in comprehensive_data.items()
                if platform in platform_list
            }
        
        return {
            "status": "success",
            "data": comprehensive_data,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "time_range": time_range,
                "platforms": platform_list,
                "total_records": sum(
                    len(table_data) if isinstance(table_data, list) else 0
                    for platform_data in comprehensive_data.values()
                    for table_data in platform_data.values()
                )
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch comprehensive data: {str(e)}")

@router.get("/platform-metrics")
async def get_platform_metrics(
    platform: str = Query(..., description="Platform name"),
    time_range: str = Query("30d", description="Time range")
):
    """Get detailed metrics for a specific platform"""
    try:
        if platform == "shopify":
            return await get_shopify_comprehensive_metrics(time_range)
        elif platform == "google_ads":
            return await get_google_ads_comprehensive_metrics(time_range)
        elif platform == "meta_ads":
            return await get_meta_ads_comprehensive_metrics(time_range)
        elif platform == "shiprocket":
            return await get_shiprocket_comprehensive_metrics(time_range)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch platform metrics: {str(e)}")

@router.post("/export-data")
async def export_data(request: DataExportRequest):
    """Export data in various formats"""
    try:
        # Implementation for data export
        export_result = await process_data_export(
            format=request.format,
            platforms=request.platforms,
            time_range=request.time_range,
            tables=request.tables
        )
        
        return {
            "status": "success",
            "export_url": export_result["url"],
            "file_size": export_result["size"],
            "format": request.format,
            "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/data-warehouse/status")
async def get_data_warehouse_status():
    """Get BigQuery data warehouse status"""
    try:
        # Sample data warehouse status
        return {
            "status": "healthy",
            "total_records": 2450000,
            "storage_used": "8.2 GB",
            "storage_limit": "100 GB",
            "active_tables": 24,
            "query_credits_used": 153,
            "query_credits_limit": 1000,
            "last_sync": datetime.utcnow().isoformat(),
            "tables": [
                {"name": "shopify_orders", "records": 125430, "size": "2.3 GB"},
                {"name": "shopify_customers", "records": 85400, "size": "450 MB"},
                {"name": "google_ads_performance", "records": 452800, "size": "1.2 GB"},
                {"name": "meta_ads_insights", "records": 389200, "size": "980 MB"},
                {"name": "shiprocket_shipments", "records": 893400, "size": "3.1 GB"},
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get warehouse status: {str(e)}")

# Helper functions for data retrieval
async def get_shopify_orders_data(time_range: str):
    """Get Shopify orders data"""
    # Sample data - replace with actual BigQuery queries
    return [
        {
            "order_id": "ORD-2024-001",
            "date": "2024-01-15",
            "customer_name": "John Doe",
            "product_name": "Premium T-Shirt",
            "quantity": 2,
            "unit_price": 1299,
            "total_amount": 2598,
            "discount": 260,
            "tax": 467,
            "shipping": 99,
            "payment_method": "Credit Card",
            "status": "Delivered",
            "channel": "Online Store",
            "location": "Mumbai, MH"
        }
        # Add more sample data...
    ]

async def get_shopify_customers_data(time_range: str):
    """Get Shopify customers data"""
    return [
        {
            "customer_id": "CUST-001",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+91-9876543210",
            "total_orders": 5,
            "total_spent": 12450,
            "avg_order_value": 2490,
            "first_order_date": "2023-08-15",
            "last_order_date": "2024-01-15",
            "customer_segment": "High Value",
            "location": "Mumbai, MH"
        }
        # Add more sample data...
    ]

async def get_shopify_products_data(time_range: str):
    """Get Shopify products data"""
    return [
        {
            "product_id": "PROD-001",
            "name": "Premium T-Shirt",
            "sku": "PTS-001",
            "category": "Apparel",
            "price": 1299,
            "cost": 450,
            "margin": 65.3,
            "units_sold": 245,
            "revenue": 318255,
            "inventory_level": 150,
            "reorder_point": 50
        }
        # Add more sample data...
    ]

async def get_shopify_inventory_data():
    """Get Shopify inventory data"""
    return [
        {
            "product_id": "PROD-001",
            "sku": "PTS-001",
            "name": "Premium T-Shirt",
            "current_stock": 150,
            "reserved": 25,
            "available": 125,
            "reorder_point": 50,
            "max_stock": 500,
            "last_restocked": "2024-01-10"
        }
        # Add more sample data...
    ]

async def get_shopify_transactions_data(time_range: str):
    """Get Shopify transactions data"""
    return [
        {
            "transaction_id": "TXN-001",
            "order_id": "ORD-2024-001",
            "date": "2024-01-15",
            "amount": 2598,
            "payment_method": "Credit Card",
            "gateway": "Razorpay",
            "status": "Completed",
            "fees": 65,
            "net_amount": 2533
        }
        # Add more sample data...
    ]

async def get_shopify_analytics_data(time_range: str):
    """Get Shopify analytics data"""
    return {
        "total_revenue": 2850000,
        "total_orders": 12450,
        "avg_order_value": 2289,
        "conversion_rate": 3.2,
        "cart_abandonment_rate": 68.5,
        "return_rate": 2.1,
        "customer_acquisition_cost": 245,
        "customer_lifetime_value": 4580
    }

async def get_google_ads_campaigns_data(time_range: str):
    """Get Google Ads campaigns data"""
    return [
        {
            "campaign_id": "12345",
            "campaign_name": "Summer Sale 2024",
            "status": "Active",
            "budget": 50000,
            "spend": 42500,
            "impressions": 125000,
            "clicks": 2340,
            "ctr": 1.87,
            "cpc": 18.16,
            "conversions": 156,
            "conversion_rate": 6.67,
            "cpa": 272.44,
            "roas": 4.2
        }
        # Add more sample data...
    ]

async def get_google_ads_adgroups_data(time_range: str):
    """Get Google Ads ad groups data"""
    return [
        {
            "ad_group_id": "67890",
            "campaign_id": "12345",
            "ad_group_name": "T-Shirts",
            "status": "Active",
            "impressions": 45000,
            "clicks": 890,
            "ctr": 1.98,
            "cpc": 15.50,
            "cost": 13795,
            "conversions": 67,
            "conversion_rate": 7.53
        }
        # Add more sample data...
    ]

async def get_google_ads_keywords_data(time_range: str):
    """Get Google Ads keywords data"""
    return [
        {
            "keyword_id": "11111",
            "keyword": "premium t-shirt",
            "match_type": "Exact",
            "impressions": 12450,
            "clicks": 234,
            "ctr": 1.88,
            "cpc": 12.50,
            "cost": 2925,
            "conversions": 18,
            "conversion_rate": 7.69,
            "quality_score": 8
        }
        # Add more sample data...
    ]

async def get_google_ads_ads_data(time_range: str):
    """Get Google Ads ads data"""
    return [
        {
            "ad_id": "22222",
            "ad_group_id": "67890",
            "headline": "Premium Quality T-Shirts",
            "description": "Shop now for the best deals",
            "status": "Active",
            "impressions": 8920,
            "clicks": 156,
            "ctr": 1.75,
            "cpc": 18.75,
            "cost": 2925
        }
        # Add more sample data...
    ]

async def get_google_ads_performance_data(time_range: str):
    """Get Google Ads performance data"""
    return [
        {
            "date": "2024-01-15",
            "impressions": 12450,
            "clicks": 234,
            "cost": 2925,
            "conversions": 18,
            "revenue": 12285
        }
        # Add more sample data...
    ]

async def get_google_ads_demographics_data(time_range: str):
    """Get Google Ads demographics data"""
    return [
        {
            "age_group": "25-34",
            "gender": "Male",
            "impressions": 5680,
            "clicks": 123,
            "conversions": 8,
            "cost": 1540
        }
        # Add more sample data...
    ]

# Similar functions for Meta Ads and Shiprocket...
async def get_meta_ads_campaigns_data(time_range: str):
    return []  # Implement similar to Google Ads

async def get_meta_ads_adsets_data(time_range: str):
    return []

async def get_meta_ads_ads_data(time_range: str):
    return []

async def get_meta_ads_insights_data(time_range: str):
    return []

async def get_meta_ads_audiences_data(time_range: str):
    return []

async def get_meta_ads_creatives_data(time_range: str):
    return []

async def get_shiprocket_shipments_data(time_range: str):
    return []

async def get_shiprocket_tracking_data(time_range: str):
    return []

async def get_shiprocket_returns_data(time_range: str):
    return []

async def get_shiprocket_couriers_data():
    return []

async def get_shiprocket_zones_data():
    return []

async def get_shiprocket_performance_data(time_range: str):
    return []

async def get_shopify_comprehensive_metrics(time_range: str):
    return {}

async def get_google_ads_comprehensive_metrics(time_range: str):
    return {}

async def get_meta_ads_comprehensive_metrics(time_range: str):
    return {}

async def get_shiprocket_comprehensive_metrics(time_range: str):
    return {}

async def process_data_export(format: str, platforms: List[str], time_range: str, tables: Optional[List[str]]):
    return {"url": "https://example.com/export.csv", "size": "2.5 MB"}