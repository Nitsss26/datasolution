from fastapi import APIRouter, Depends
from typing import Dict, Any
from utils.auth import verify_token
from models.analytics import DashboardMetrics, ChartData
import random
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    time_range: str = "30d",
    current_user: str = Depends(verify_token)
):
    # Mock data - replace with actual database queries
    return DashboardMetrics(
        total_revenue=125000.50,
        total_orders=1250,
        average_order_value=100.00,
        conversion_rate=3.5,
        return_on_ad_spend=4.2,
        customer_acquisition_cost=25.00
    )

@router.get("/charts/revenue", response_model=ChartData)
async def get_revenue_chart(
    time_range: str = "30d",
    current_user: str = Depends(verify_token)
):
    # Generate mock data for the last 30 days
    days = 30 if time_range == "30d" else 7
    labels = []
    data = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        labels.append(date.strftime("%Y-%m-%d"))
        data.append(random.randint(1000, 5000))
    
    return ChartData(
        labels=labels,
        datasets=[
            {
                "label": "Revenue",
                "data": data,
                "borderColor": "rgb(59, 130, 246)",
                "backgroundColor": "rgba(59, 130, 246, 0.1)",
                "tension": 0.4
            }
        ]
    )

@router.get("/charts/orders", response_model=ChartData)
async def get_orders_chart(
    time_range: str = "30d",
    current_user: str = Depends(verify_token)
):
    days = 30 if time_range == "30d" else 7
    labels = []
    data = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        labels.append(date.strftime("%Y-%m-%d"))
        data.append(random.randint(10, 50))
    
    return ChartData(
        labels=labels,
        datasets=[
            {
                "label": "Orders",
                "data": data,
                "borderColor": "rgb(16, 185, 129)",
                "backgroundColor": "rgba(16, 185, 129, 0.1)",
                "tension": 0.4
            }
        ]
    )

@router.get("/charts/conversion", response_model=ChartData)
async def get_conversion_chart(
    time_range: str = "30d",
    current_user: str = Depends(verify_token)
):
    days = 30 if time_range == "30d" else 7
    labels = []
    data = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i-1)
        labels.append(date.strftime("%Y-%m-%d"))
        data.append(round(random.uniform(2.0, 5.0), 2))
    
    return ChartData(
        labels=labels,
        datasets=[
            {
                "label": "Conversion Rate (%)",
                "data": data,
                "borderColor": "rgb(245, 158, 11)",
                "backgroundColor": "rgba(245, 158, 11, 0.1)",
                "tension": 0.4
            }
        ]
    )
