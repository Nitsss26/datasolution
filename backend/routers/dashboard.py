from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.analytics import DashboardData, TimeRange, Platform, MetricData, ChartData
from utils.auth import verify_token
from database import get_database
import random
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/metrics", response_model=DashboardData)
async def get_dashboard_metrics(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    platforms: str = "shopify,facebook_ads,google_ads",
    current_user: str = Depends(verify_token)
):
    """Get dashboard metrics for specified platforms and time range"""
    
    # Parse platforms
    platform_list = [Platform(p.strip()) for p in platforms.split(",")]
    
    # Generate mock data (replace with actual data fetching logic)
    metrics = []
    
    # Revenue metrics
    total_revenue = random.uniform(50000, 200000)
    metrics.append(MetricData(
        metric="revenue",
        value=total_revenue,
        change_percentage=random.uniform(-10, 25)
    ))
    
    # Orders
    total_orders = random.randint(500, 2000)
    metrics.append(MetricData(
        metric="orders",
        value=total_orders,
        change_percentage=random.uniform(-5, 30)
    ))
    
    # AOV
    aov = total_revenue / total_orders
    metrics.append(MetricData(
        metric="aov",
        value=aov,
        change_percentage=random.uniform(-8, 15)
    ))
    
    # ROAS
    metrics.append(MetricData(
        metric="roas",
        value=random.uniform(3.5, 8.0),
        change_percentage=random.uniform(-15, 20)
    ))
    
    # Generate chart data
    days = int(time_range.value.replace('d', ''))
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days, 0, -1)]
    
    revenue_chart = ChartData(
        labels=dates,
        datasets=[{
            "label": "Revenue",
            "data": [random.uniform(1000, 5000) for _ in dates],
            "borderColor": "rgb(59, 130, 246)",
            "backgroundColor": "rgba(59, 130, 246, 0.1)"
        }]
    )
    
    orders_chart = ChartData(
        labels=dates,
        datasets=[{
            "label": "Orders",
            "data": [random.randint(10, 50) for _ in dates],
            "borderColor": "rgb(16, 185, 129)",
            "backgroundColor": "rgba(16, 185, 129, 0.1)"
        }]
    )
    
    platform_revenue_chart = ChartData(
        labels=[p.value.replace('_', ' ').title() for p in platform_list],
        datasets=[{
            "label": "Revenue by Platform",
            "data": [random.uniform(10000, 50000) for _ in platform_list],
            "backgroundColor": [
                "rgba(59, 130, 246, 0.8)",
                "rgba(16, 185, 129, 0.8)",
                "rgba(245, 158, 11, 0.8)",
                "rgba(239, 68, 68, 0.8)"
            ]
        }]
    )
    
    charts = {
        "revenue_trend": revenue_chart,
        "orders_trend": orders_chart,
        "platform_revenue": platform_revenue_chart
    }
    
    return DashboardData(metrics=metrics, charts=charts)

@router.get("/summary")
async def get_dashboard_summary(current_user: str = Depends(verify_token)):
    """Get dashboard summary statistics"""
    return {
        "total_revenue": random.uniform(100000, 500000),
        "total_orders": random.randint(1000, 5000),
        "active_platforms": 4,
        "conversion_rate": random.uniform(2.5, 8.0),
        "last_sync": datetime.utcnow().isoformat()
    }
