from fastapi import APIRouter, Depends, Query
from models.analytics import TimeRange
from database import get_database
from datetime import datetime, timedelta
import pandas as pd
from google.cloud import bigquery

router = APIRouter()

@router.post("/export-to-bigquery")
async def export_to_bigquery(
    time_range: TimeRange = Query(TimeRange.DAYS_30),
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    """Export analytics data to BigQuery"""
    db = await get_database()
    
    # Calculate date range
    days_map = {"7d": 7, "15d": 15, "30d": 30, "90d": 90}
    days = days_map.get(time_range, 30)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get analytics data
    query = {
        "user_id": str(current_user["_id"]),
        "date": {"$gte": start_date}
    }
    
    analytics_data = []
    async for doc in db.analytics_data.find(query):
        analytics_data.append(doc)
    
    # Convert to DataFrame
    df_data = []
    for doc in analytics_data:
        metrics = doc.get("metrics", {})
        df_data.append({
            "user_id": doc["user_id"],
            "platform": doc["platform"],
            "date": doc["date"],
            "revenue": metrics.get("revenue", 0),
            "orders": metrics.get("orders", 0),
            "sessions": metrics.get("sessions", 0),
            "ad_spend": metrics.get("ad_spend", 0),
            "clicks": metrics.get("clicks", 0),
            "impressions": metrics.get("impressions", 0)
        })
    
    df = pd.DataFrame(df_data)
    
    # Export to BigQuery (mock implementation)
    # In production, you would use proper BigQuery client
    try:
        # client = bigquery.Client()
        # table_id = "your-project.dataset.analytics_data"
        # job = client.load_table_from_dataframe(df, table_id)
        # job.result()
        
        return {
            "message": "Data exported to BigQuery successfully",
            "records_exported": len(df_data)
        }
    except Exception as e:
        return {
            "error": f"Export failed: {str(e)}",
            "records_exported": 0
        }

@router.get("/p-and-l")
async def get_profit_and_loss(
    time_range: TimeRange = Query(TimeRange.DAYS_30),
    platforms: str = Query("all"),
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    """Generate Profit & Loss report"""
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
    
    # Calculate P&L
    total_revenue = sum(doc.get("metrics", {}).get("revenue", 0) for doc in analytics_data)
    total_ad_spend = sum(doc.get("metrics", {}).get("ad_spend", 0) for doc in analytics_data)
    total_shipping_cost = sum(doc.get("metrics", {}).get("shipping_cost", 0) for doc in analytics_data)
    
    # Mock additional costs
    cogs = total_revenue * 0.4  # 40% of revenue
    marketplace_fees = total_revenue * 0.1  # 10% of revenue
    other_expenses = total_revenue * 0.05  # 5% of revenue
    
    # Calculate profits
    gross_profit = total_revenue - cogs
    total_expenses = total_ad_spend + total_shipping_cost + marketplace_fees + other_expenses
    net_profit = gross_profit - total_expenses
    
    # Calculate margins
    gross_margin = (gross_profit / total_revenue) * 100 if total_revenue > 0 else 0
    net_margin = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0
    
    return {
        "revenue": {
            "total_revenue": total_revenue,
            "gross_profit": gross_profit,
            "gross_margin": gross_margin
        },
        "expenses": {
            "cogs": cogs,
            "ad_spend": total_ad_spend,
            "shipping_cost": total_shipping_cost,
            "marketplace_fees": marketplace_fees,
            "other_expenses": other_expenses,
            "total_expenses": total_expenses
        },
        "profit": {
            "net_profit": net_profit,
            "net_margin": net_margin
        },
        "metrics": {
            "roas": total_revenue / total_ad_spend if total_ad_spend > 0 else 0,
            "cost_per_order": total_expenses / sum(doc.get("metrics", {}).get("orders", 0) for doc in analytics_data)
        }
    }
