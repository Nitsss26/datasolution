from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from models.analytics import TimeRange, Platform, AnalyticsRequest
from utils.auth import verify_token
from database import get_database
import random
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/query")
async def query_analytics(
    request: AnalyticsRequest,
    current_user: str = Depends(verify_token)
):
    """Query analytics data based on specified criteria"""
    
    # This would typically query BigQuery or your data warehouse
    # For now, returning mock data
    
    results = {}
    
    for metric in request.metrics:
        if metric == "revenue":
            results[metric] = {
                "total": random.uniform(50000, 200000),
                "by_platform": {platform.value: random.uniform(10000, 50000) for platform in request.platforms}
            }
        elif metric == "orders":
            results[metric] = {
                "total": random.randint(500, 2000),
                "by_platform": {platform.value: random.randint(100, 500) for platform in request.platforms}
            }
        elif metric == "aov":
            results[metric] = {
                "average": random.uniform(80, 250),
                "by_platform": {platform.value: random.uniform(80, 250) for platform in request.platforms}
            }
        elif metric == "roas":
            results[metric] = {
                "average": random.uniform(3.0, 8.0),
                "by_platform": {platform.value: random.uniform(3.0, 8.0) for platform in request.platforms}
            }
    
    return {
        "data": results,
        "time_range": request.time_range,
        "platforms": request.platforms,
        "generated_at": datetime.utcnow()
    }

@router.get("/profit-loss")
async def get_profit_loss(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    platforms: str = Query("shopify,facebook_ads,google_ads"),
    current_user: str = Depends(verify_token)
):
    """Generate P&L report"""
    
    platform_list = [Platform(p.strip()) for p in platforms.split(",")]
    
    # Mock P&L data
    revenue = random.uniform(100000, 300000)
    cogs = revenue * random.uniform(0.3, 0.5)
    ad_spend = random.uniform(10000, 30000)
    marketplace_fees = revenue * random.uniform(0.05, 0.15)
    shipping_costs = random.uniform(5000, 15000)
    other_costs = random.uniform(2000, 8000)
    
    gross_profit = revenue - cogs
    net_profit = gross_profit - ad_spend - marketplace_fees - shipping_costs - other_costs
    
    return {
        "revenue": revenue,
        "cost_of_goods_sold": cogs,
        "gross_profit": gross_profit,
        "gross_margin": (gross_profit / revenue) * 100,
        "expenses": {
            "ad_spend": ad_spend,
            "marketplace_fees": marketplace_fees,
            "shipping_costs": shipping_costs,
            "other_costs": other_costs
        },
        "net_profit": net_profit,
        "net_margin": (net_profit / revenue) * 100,
        "time_range": time_range,
        "platforms": platform_list,
        "generated_at": datetime.utcnow()
    }

@router.get("/export/csv")
async def export_analytics_csv(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    platforms: str = Query("shopify,facebook_ads,google_ads"),
    current_user: str = Depends(verify_token)
):
    """Export analytics data as CSV"""
    
    # This would generate and return a CSV file
    # For now, return a success message
    
    return {
        "message": "CSV export initiated",
        "download_url": "/api/analytics/download/analytics_export.csv",
        "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }
