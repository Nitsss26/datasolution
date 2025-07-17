from fastapi import APIRouter, Query
from typing import Optional
from models.analytics import MetricData, ChartDataPoint, PlatformMetric
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/metrics")
async def get_dashboard_metrics(
    time_range: Optional[str] = Query("30d", regex="^(7d|15d|30d|90d)$")
):
    # Mock data - replace with actual database queries
    return {
        "total_revenue": {
            "value": 125000.50,
            "change": 12.5,
            "trend": "up"
        },
        "total_orders": {
            "value": 1250,
            "change": 8.3,
            "trend": "up"
        },
        "average_order_value": {
            "value": 100.00,
            "change": 3.8,
            "trend": "up"
        },
        "conversion_rate": {
            "value": 3.2,
            "change": -0.5,
            "trend": "down"
        },
        "customer_acquisition_cost": {
            "value": 25.50,
            "change": -5.2,
            "trend": "down"
        },
        "return_on_ad_spend": {
            "value": 4.2,
            "change": 15.8,
            "trend": "up"
        }
    }

@router.get("/charts/revenue")
async def get_revenue_chart(
    time_range: Optional[str] = Query("30d", regex="^(7d|15d|30d|90d)$")
):
    # Generate mock data based on time range
    days = int(time_range.replace('d', ''))
    data = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i-1)).strftime("%Y-%m-%d")
        value = random.uniform(3000, 5000)
        data.append({"date": date, "value": round(value, 2)})
    
    return {"data": data}

@router.get("/charts/platforms")
async def get_platform_metrics():
    return {
        "data": [
            {
                "platform": "Shopify",
                "revenue": 75000.00,
                "orders": 750,
                "aov": 100.00,
                "roas": 4.5
            },
            {
                "platform": "Facebook Ads",
                "revenue": 30000.00,
                "orders": 300,
                "aov": 100.00,
                "roas": 3.8
            },
            {
                "platform": "Google Ads",
                "revenue": 20000.00,
                "orders": 200,
                "aov": 100.00,
                "roas": 4.2
            }
        ]
    }

@router.get("/charts/conversion-funnel")
async def get_conversion_funnel():
    return {
        "data": [
            {"stage": "Visitors", "value": 10000, "percentage": 100},
            {"stage": "Product Views", "value": 5000, "percentage": 50},
            {"stage": "Add to Cart", "value": 1500, "percentage": 15},
            {"stage": "Checkout", "value": 500, "percentage": 5},
            {"stage": "Purchase", "value": 320, "percentage": 3.2}
        ]
    }

@router.get("/charts/customer-segments")
async def get_customer_segments():
    return {
        "data": [
            {"segment": "New Customers", "count": 450, "revenue": 45000, "percentage": 36},
            {"segment": "Returning Customers", "count": 600, "revenue": 60000, "percentage": 48},
            {"segment": "VIP Customers", "count": 200, "revenue": 20000, "percentage": 16}
        ]
    }
