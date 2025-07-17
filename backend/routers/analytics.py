from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from utils.auth import verify_token
from models.analytics import MetricData, ChartData
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/metrics/{metric_type}", response_model=List[MetricData])
async def get_metric_data(
    metric_type: str,
    time_range: str = "30d",
    platform: str = None,
    current_user: str = Depends(verify_token)
):
    # Mock data generation
    days = 30 if time_range == "30d" else 7
    metrics = []
    
    platforms = ["shopify", "facebook", "google"] if not platform else [platform]
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        for plat in platforms:
            value = random.uniform(100, 1000) if metric_type == "revenue" else random.randint(1, 50)
            metrics.append(MetricData(
                date=date,
                value=value,
                platform=plat,
                metric_type=metric_type
            ))
    
    return metrics

@router.get("/export/{format}")
async def export_data(
    format: str,
    time_range: str = "30d",
    current_user: str = Depends(verify_token)
):
    if format not in ["csv", "xlsx", "pdf"]:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    # Mock export functionality
    return {"message": f"Export in {format} format initiated", "download_url": f"/downloads/export.{format}"}

@router.get("/summary", response_model=Dict[str, Any])
async def get_analytics_summary(
    time_range: str = "30d",
    current_user: str = Depends(verify_token)
):
    return {
        "total_revenue": 125000.50,
        "total_orders": 1250,
        "top_platform": "shopify",
        "growth_rate": 15.5,
        "period": time_range
    }
