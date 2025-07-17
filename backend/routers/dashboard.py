from fastapi import APIRouter, Depends, HTTPException, Query
from models.analytics import TimeRange, DashboardMetrics, PlatformMetrics
from database import get_database
from datetime import datetime, timedelta
import numpy as np

router = APIRouter()

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    time_range: TimeRange = Query(TimeRange.DAYS_30),
    platforms: str = Query("all"),
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    db = await get_database()
    
    # Calculate date range
    days_map = {"7d": 7, "15d": 15, "30d": 30, "90d": 90}
    days = days_map.get(time_range, 30)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Parse platforms
    if platforms == "all":
        platform_filter = {}
    else:
        platform_list = platforms.split(",")
        platform_filter = {"platform": {"$in": platform_list}}
    
    # Build query
    query = {
        "user_id": str(current_user["_id"]),
        "date": {"$gte": start_date},
        **platform_filter
    }
    
    # Get analytics data
    analytics_data = []
    async for doc in db.analytics_data.find(query):
        analytics_data.append(doc)
    
    # Calculate metrics
    total_revenue = sum(doc.get("metrics", {}).get("revenue", 0) for doc in analytics_data)
    total_orders = sum(doc.get("metrics", {}).get("orders", 0) for doc in analytics_data)
    total_ad_spend = sum(doc.get("metrics", {}).get("ad_spend", 0) for doc in analytics_data)
    total_sessions = sum(doc.get("metrics", {}).get("sessions", 0) for doc in analytics_data)
    total_clicks = sum(doc.get("metrics", {}).get("clicks", 0) for doc in analytics_data)
    
    # Calculate derived metrics
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    roas = total_revenue / total_ad_spend if total_ad_spend > 0 else 0
    conversion_rate = (total_orders / total_sessions) * 100 if total_sessions > 0 else 0
    bounce_rate = np.random.uniform(35, 65)  # Mock bounce rate
    
    return DashboardMetrics(
        total_revenue=total_revenue,
        total_orders=total_orders,
        avg_order_value=avg_order_value,
        total_ad_spend=total_ad_spend,
        roas=roas,
        conversion_rate=conversion_rate,
        total_sessions=total_sessions,
        bounce_rate=bounce_rate
    )

@router.get("/platform-metrics")
async def get_platform_metrics(
    time_range: TimeRange = Query(TimeRange.DAYS_30),
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    db = await get_database()
    
    # Calculate date range
    days_map = {"7d": 7, "15d": 15, "30d": 30, "90d": 90}
    days = days_map.get(time_range, 30)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Aggregate by platform
    pipeline = [
        {
            "$match": {
                "user_id": str(current_user["_id"]),
                "date": {"$gte": start_date}
            }
        },
        {
            "$group": {
                "_id": "$platform",
                "revenue": {"$sum": "$metrics.revenue"},
                "orders": {"$sum": "$metrics.orders"},
                "sessions": {"$sum": "$metrics.sessions"},
                "clicks": {"$sum": "$metrics.clicks"}
            }
        }
    ]
    
    results = []
    async for doc in db.analytics_data.aggregate(pipeline):
        conversion_rate = (doc["orders"] / doc["sessions"]) * 100 if doc["sessions"] > 0 else 0
        results.append(PlatformMetrics(
            platform=doc["_id"],
            revenue=doc["revenue"],
            orders=doc["orders"],
            sessions=doc["sessions"],
            conversion_rate=conversion_rate
        ))
    
    return results

@router.get("/chart-data")
async def get_chart_data(
    chart_type: str = Query("revenue_trend"),
    time_range: TimeRange = Query(TimeRange.DAYS_30),
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    db = await get_database()
    
    # Calculate date range
    days_map = {"7d": 7, "15d": 15, "30d": 30, "90d": 90}
    days = days_map.get(time_range, 30)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    if chart_type == "revenue_trend":
        # Daily revenue trend
        pipeline = [
            {
                "$match": {
                    "user_id": str(current_user["_id"]),
                    "date": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$date"
                        }
                    },
                    "revenue": {"$sum": "$metrics.revenue"}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        results = []
        async for doc in db.analytics_data.aggregate(pipeline):
            results.append({
                "date": doc["_id"],
                "revenue": doc["revenue"]
            })
        
        return results
    
    elif chart_type == "platform_revenue":
        # Revenue by platform
        pipeline = [
            {
                "$match": {
                    "user_id": str(current_user["_id"]),
                    "date": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": "$platform",
                    "revenue": {"$sum": "$metrics.revenue"}
                }
            }
        ]
        
        results = []
        async for doc in db.analytics_data.aggregate(pipeline):
            results.append({
                "platform": doc["_id"],
                "revenue": doc["revenue"]
            })
        
        return results
    
    else:
        raise HTTPException(status_code=400, detail="Invalid chart type")
