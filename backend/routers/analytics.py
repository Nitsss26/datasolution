from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from utils.data_processor import DataProcessor
from utils.bigquery_client import BigQueryClient
from database import get_database

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
bigquery_client = BigQueryClient()
data_processor = DataProcessor(bigquery_client)

class AnalyticsRequest(BaseModel):
    platforms: List[str] = ["all"]
    time_range: str = "30d"
    metrics: Optional[List[str]] = None
    granularity: str = "daily"

class AnalyticsResponse(BaseModel):
    d2cMetrics: Dict[str, Any]
    adMetrics: Dict[str, Any]
    deliveryMetrics: Dict[str, Any]
    trends: Dict[str, Any]
    platformBreakdown: Dict[str, Any]
    timeSeriesData: List[Dict[str, Any]]
    summary: Dict[str, Any]

@router.post("/", response_model=AnalyticsResponse)
async def get_analytics(request: AnalyticsRequest):
    """Get comprehensive analytics data"""
    try:
        logger.info(f"Analytics request: platforms={request.platforms}, time_range={request.time_range}")
        
        # Get analytics data from data processor
        analytics_data = await data_processor.get_analytics(
            platforms=request.platforms,
            time_range=request.time_range,
            metrics=request.metrics,
            granularity=request.granularity
        )
        
        return analytics_data
        
    except Exception as e:
        logger.error(f"Analytics fetch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics fetch failed: {str(e)}")

@router.get("/summary")
async def get_analytics_summary():
    """Get quick analytics summary"""
    try:
        # Get summary data for dashboard cards
        summary_data = await data_processor.get_analytics(
            platforms=["all"],
            time_range="30d",
            metrics=["totalRevenue", "totalOrders", "newCustomerCount", "returnOnAdSpend"]
        )
        
        return {
            "totalRevenue": summary_data.get("d2cMetrics", {}).get("totalRevenue", 0),
            "totalOrders": summary_data.get("d2cMetrics", {}).get("totalOrders", 0),
            "newCustomers": summary_data.get("d2cMetrics", {}).get("newCustomerCount", 0),
            "roas": summary_data.get("adMetrics", {}).get("returnOnAdSpend", 0),
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Summary fetch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Summary fetch failed: {str(e)}")

@router.get("/trends/{metric}")
async def get_metric_trend(metric: str, time_range: str = "30d", platforms: str = "all"):
    """Get trend data for a specific metric"""
    try:
        platform_list = platforms.split(",") if platforms != "all" else ["all"]
        
        analytics_data = await data_processor.get_analytics(
            platforms=platform_list,
            time_range=time_range,
            metrics=[metric]
        )
        
        trend_data = analytics_data.get("trends", {}).get(metric, [])
        
        return {
            "metric": metric,
            "time_range": time_range,
            "platforms": platform_list,
            "data": trend_data,
            "currency": "INR" if "revenue" in metric.lower() or "cost" in metric.lower() else None
        }
        
    except Exception as e:
        logger.error(f"Trend fetch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Trend fetch failed: {str(e)}")

@router.get("/platforms/{platform_id}")
async def get_platform_analytics(platform_id: str, time_range: str = "30d"):
    """Get analytics for a specific platform"""
    try:
        analytics_data = await data_processor.get_analytics(
            platforms=[platform_id],
            time_range=time_range
        )
        
        platform_data = analytics_data.get("platformBreakdown", {}).get(platform_id, {})
        
        return {
            "platform": platform_id,
            "time_range": time_range,
            "data": platform_data,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Platform analytics fetch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Platform analytics fetch failed: {str(e)}")

@router.post("/custom-query")
async def execute_custom_query(query_data: Dict[str, Any]):
    """Execute custom analytics query"""
    try:
        sql_query = query_data.get("sql_query")
        if not sql_query:
            raise HTTPException(status_code=400, detail="SQL query is required")
        
        # Execute custom query through BigQuery
        results = await bigquery_client.query_data(sql_query)
        
        return {
            "query": sql_query,
            "results": results,
            "row_count": len(results),
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Custom query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Custom query failed: {str(e)}")

@router.get("/export/{format}")
async def export_analytics(format: str, platforms: str = "all", time_range: str = "30d"):
    """Export analytics data in specified format"""
    try:
        if format not in ["json", "csv", "excel"]:
            raise HTTPException(status_code=400, detail="Unsupported export format")
        
        platform_list = platforms.split(",") if platforms != "all" else ["all"]
        
        analytics_data = await data_processor.get_analytics(
            platforms=platform_list,
            time_range=time_range
        )
        
        # Add export metadata
        export_data = {
            "exported_at": datetime.utcnow().isoformat(),
            "platforms": platform_list,
            "time_range": time_range,
            "currency": "INR",
            "data": analytics_data
        }
        
        return export_data
        
    except Exception as e:
        logger.error(f"Export failed: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")