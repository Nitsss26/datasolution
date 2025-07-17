from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timedelta
from utils.auth import verify_token
from database import get_database
import random

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_data = await verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return token_data

@router.get("/metrics")
async def get_dashboard_metrics(
    time_range: str = Query("7d", regex="^(7d|15d|30d|90d)$"),
    current_user: dict = Depends(get_current_user)
):
    """Get dashboard metrics for specified time range"""
    
    # Generate mock data based on time range
    days = int(time_range.replace('d', ''))
    
    # Mock metrics - in production, fetch from database
    metrics = {
        "total_revenue": round(random.uniform(10000, 50000) * (days / 7), 2),
        "total_orders": random.randint(100, 500) * (days // 7),
        "avg_order_value": round(random.uniform(50, 200), 2),
        "conversion_rate": round(random.uniform(2, 8), 2),
        "roas": round(random.uniform(3, 8), 2),
        "acos": round(random.uniform(15, 35), 2),
        "growth_rate": round(random.uniform(-10, 25), 2),
        "customer_acquisition_cost": round(random.uniform(20, 80), 2)
    }
    
    return metrics

@router.get("/charts/revenue")
async def get_revenue_chart(
    time_range: str = Query("7d", regex="^(7d|15d|30d|90d)$"),
    current_user: dict = Depends(get_current_user)
):
    """Get revenue chart data"""
    
    days = int(time_range.replace('d', ''))
    
    # Generate mock chart data
    labels = []
    revenue_data = []
    orders_data = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        labels.append(date.strftime("%Y-%m-%d"))
        revenue_data.append(round(random.uniform(500, 2000), 2))
        orders_data.append(random.randint(10, 50))
    
    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Revenue",
                "data": revenue_data,
                "borderColor": "rgb(59, 130, 246)",
                "backgroundColor": "rgba(59, 130, 246, 0.1)",
                "tension": 0.4
            },
            {
                "label": "Orders",
                "data": orders_data,
                "borderColor": "rgb(16, 185, 129)",
                "backgroundColor": "rgba(16, 185, 129, 0.1)",
                "tension": 0.4,
                "yAxisID": "y1"
            }
        ]
    }

@router.get("/charts/platforms")
async def get_platform_chart(
    time_range: str = Query("7d", regex="^(7d|15d|30d|90d)$"),
    current_user: dict = Depends(get_current_user)
):
    """Get platform comparison chart data"""
    
    platforms = ["Shopify", "Facebook Ads", "Google Ads", "Shiprocket"]
    
    return {
        "labels": platforms,
        "datasets": [
            {
                "label": "Revenue",
                "data": [
                    round(random.uniform(5000, 15000), 2),
                    round(random.uniform(3000, 8000), 2),
                    round(random.uniform(2000, 6000), 2),
                    round(random.uniform(1000, 3000), 2)
                ],
                "backgroundColor": [
                    "rgba(59, 130, 246, 0.8)",
                    "rgba(16, 185, 129, 0.8)",
                    "rgba(245, 158, 11, 0.8)",
                    "rgba(239, 68, 68, 0.8)"
                ]
            }
        ]
    }

@router.get("/charts/conversion")
async def get_conversion_funnel(
    time_range: str = Query("7d", regex="^(7d|15d|30d|90d)$"),
    current_user: dict = Depends(get_current_user)
):
    """Get conversion funnel data"""
    
    return {
        "labels": ["Visitors", "Add to Cart", "Checkout", "Purchase"],
        "datasets": [
            {
                "label": "Conversion Funnel",
                "data": [10000, 3000, 1200, 800],
                "backgroundColor": [
                    "rgba(59, 130, 246, 0.8)",
                    "rgba(16, 185, 129, 0.8)",
                    "rgba(245, 158, 11, 0.8)",
                    "rgba(34, 197, 94, 0.8)"
                ]
            }
        ]
    }

@router.get("/platform-metrics")
async def get_platform_metrics(
    time_range: str = Query("7d", regex="^(7d|15d|30d|90d)$"),
    current_user: dict = Depends(get_current_user)
):
    """Get detailed platform metrics"""
    
    platforms = [
        {
            "platform": "Shopify",
            "revenue": round(random.uniform(8000, 15000), 2),
            "orders": random.randint(150, 300),
            "roas": round(random.uniform(4, 7), 2),
            "spend": round(random.uniform(2000, 4000), 2),
            "conversion_rate": round(random.uniform(3, 6), 2)
        },
        {
            "platform": "Facebook Ads",
            "revenue": round(random.uniform(5000, 10000), 2),
            "orders": random.randint(100, 200),
            "roas": round(random.uniform(3, 6), 2),
            "spend": round(random.uniform(1500, 3000), 2),
            "conversion_rate": round(random.uniform(2, 5), 2)
        },
        {
            "platform": "Google Ads",
            "revenue": round(random.uniform(3000, 8000), 2),
            "orders": random.randint(80, 150),
            "roas": round(random.uniform(3.5, 6.5), 2),
            "spend": round(random.uniform(1000, 2500), 2),
            "conversion_rate": round(random.uniform(2.5, 5.5), 2)
        },
        {
            "platform": "Shiprocket",
            "revenue": round(random.uniform(2000, 5000), 2),
            "orders": random.randint(50, 120),
            "roas": round(random.uniform(2, 4), 2),
            "spend": round(random.uniform(800, 1800), 2),
            "conversion_rate": round(random.uniform(1.5, 4), 2)
        }
    ]
    
    return platforms
