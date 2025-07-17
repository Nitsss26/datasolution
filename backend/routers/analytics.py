from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
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

@router.get("/overview")
async def get_analytics_overview(
    time_range: str = Query("30d", regex="^(7d|15d|30d|90d)$"),
    current_user: dict = Depends(get_current_user)
):
    """Get analytics overview"""
    
    days = int(time_range.replace('d', ''))
    
    return {
        "summary": {
            "total_revenue": round(random.uniform(20000, 80000) * (days / 30), 2),
            "total_orders": random.randint(500, 2000) * (days // 30),
            "unique_customers": random.randint(300, 1200) * (days // 30),
            "avg_order_value": round(random.uniform(60, 180), 2),
            "customer_lifetime_value": round(random.uniform(200, 600), 2),
            "retention_rate": round(random.uniform(25, 45), 2)
        },
        "growth": {
            "revenue_growth": round(random.uniform(-5, 25), 2),
            "order_growth": round(random.uniform(-3, 20), 2),
            "customer_growth": round(random.uniform(0, 30), 2)
        }
    }

@router.get("/customer-segments")
async def get_customer_segments(
    current_user: dict = Depends(get_current_user)
):
    """Get customer segmentation data"""
    
    return {
        "segments": [
            {
                "name": "High Value",
                "count": random.randint(50, 150),
                "avg_order_value": round(random.uniform(200, 400), 2),
                "total_revenue": round(random.uniform(15000, 35000), 2),
                "percentage": round(random.uniform(15, 25), 1)
            },
            {
                "name": "Regular",
                "count": random.randint(200, 400),
                "avg_order_value": round(random.uniform(80, 150), 2),
                "total_revenue": round(random.uniform(20000, 45000), 2),
                "percentage": round(random.uniform(40, 60), 1)
            },
            {
                "name": "New",
                "count": random.randint(100, 250),
                "avg_order_value": round(random.uniform(40, 80), 2),
                "total_revenue": round(random.uniform(8000, 18000), 2),
                "percentage": round(random.uniform(20, 35), 1)
            }
        ]
    }

@router.get("/product-performance")
async def get_product_performance(
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_user)
):
    """Get top performing products"""
    
    products = []
    for i in range(limit):
        products.append({
            "product_id": f"prod_{i+1}",
            "name": f"Product {i+1}",
            "revenue": round(random.uniform(1000, 8000), 2),
            "units_sold": random.randint(50, 300),
            "avg_price": round(random.uniform(30, 150), 2),
            "profit_margin": round(random.uniform(20, 60), 2)
        })
    
    return {"products": sorted(products, key=lambda x: x["revenue"], reverse=True)}

@router.get("/cohort-analysis")
async def get_cohort_analysis(
    current_user: dict = Depends(get_current_user)
):
    """Get customer cohort analysis"""
    
    cohorts = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    
    for i, month in enumerate(months):
        retention_rates = []
        for j in range(6 - i):
            if j == 0:
                retention_rates.append(100)
            else:
                retention_rates.append(round(100 * (0.8 ** j) + random.uniform(-5, 5), 1))
        
        cohorts.append({
            "cohort": month,
            "customers": random.randint(100, 300),
            "retention_rates": retention_rates
        })
    
    return {"cohorts": cohorts}

@router.get("/export")
async def export_analytics(
    format: str = Query("csv", regex="^(csv|xlsx|json)$"),
    time_range: str = Query("30d", regex="^(7d|15d|30d|90d)$"),
    current_user: dict = Depends(get_current_user)
):
    """Export analytics data"""
    
    # In production, generate actual export file
    return {
        "message": f"Analytics data exported successfully in {format.upper()} format",
        "download_url": f"/downloads/analytics_{time_range}_{datetime.now().strftime('%Y%m%d')}.{format}",
        "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
    }

@router.get("/metrics/{metric_type}", response_model=List[dict])
async def get_metric_data(
    metric_type: str,
    time_range: str = "30d",
    platform: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    # Mock data generation
    days = 30 if time_range == "30d" else 7
    metrics = []
    
    platforms = ["shopify", "facebook", "google"] if not platform else [platform]
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        for plat in platforms:
            value = random.uniform(100, 1000) if metric_type == "revenue" else random.randint(1, 50)
            metrics.append({
                "date": date,
                "value": value,
                "platform": plat,
                "metric_type": metric_type
            })
    
    return metrics

@router.get("/summary", response_model=dict)
async def get_analytics_summary(
    time_range: str = "30d",
    current_user: dict = Depends(get_current_user)
):
    return {
        "total_revenue": 125000.50,
        "total_orders": 1250,
        "top_platform": "shopify",
        "growth_rate": 15.5,
        "period": time_range
    }
