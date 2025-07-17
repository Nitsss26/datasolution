from fastapi import APIRouter, Query
from typing import Optional, List
from models.analytics import CustomerSegment, ProductPerformance
import random

router = APIRouter()

@router.get("/overview")
async def get_analytics_overview(
    time_range: Optional[str] = Query("30d", regex="^(7d|15d|30d|90d)$")
):
    return {
        "summary": {
            "total_customers": 1250,
            "new_customers": 450,
            "returning_customers": 600,
            "customer_lifetime_value": 250.00,
            "churn_rate": 5.2
        },
        "top_products": [
            {"name": "Product A", "revenue": 25000, "units": 250},
            {"name": "Product B", "revenue": 20000, "units": 200},
            {"name": "Product C", "revenue": 15000, "units": 150}
        ],
        "traffic_sources": [
            {"source": "Organic Search", "visitors": 5000, "percentage": 50},
            {"source": "Facebook Ads", "visitors": 2000, "percentage": 20},
            {"source": "Google Ads", "visitors": 1500, "percentage": 15},
            {"source": "Direct", "visitors": 1000, "percentage": 10},
            {"source": "Email", "visitors": 500, "percentage": 5}
        ]
    }

@router.get("/customer-segments")
async def get_customer_segments():
    return {
        "segments": [
            {
                "segment": "High Value",
                "count": 200,
                "revenue": 50000,
                "percentage": 16,
                "avg_order_value": 250
            },
            {
                "segment": "Regular",
                "count": 600,
                "revenue": 60000,
                "percentage": 48,
                "avg_order_value": 100
            },
            {
                "segment": "New",
                "count": 450,
                "revenue": 15000,
                "percentage": 36,
                "avg_order_value": 33
            }
        ]
    }

@router.get("/product-performance")
async def get_product_performance(
    limit: Optional[int] = Query(10, ge=1, le=50)
):
    products = []
    for i in range(limit):
        products.append({
            "product_name": f"Product {chr(65 + i)}",
            "revenue": round(random.uniform(5000, 25000), 2),
            "units_sold": random.randint(50, 250),
            "profit_margin": round(random.uniform(20, 60), 1)
        })
    
    return {"products": products}

@router.get("/cohort-analysis")
async def get_cohort_analysis():
    return {
        "cohorts": [
            {"month": "2024-01", "customers": 100, "retention_rate": 85},
            {"month": "2024-02", "customers": 120, "retention_rate": 82},
            {"month": "2024-03", "customers": 150, "retention_rate": 78},
            {"month": "2024-04", "customers": 180, "retention_rate": 75}
        ]
    }
