from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from ..integrations.shiprocket_client import ShiprocketClient
from ..database import log_sync_operation, update_platform_sync_time

logger = logging.getLogger(__name__)

router = APIRouter()
shiprocket_client = ShiprocketClient()

class SyncRequest(BaseModel):
    force_refresh: bool = False
    limit: Optional[int] = 100

@router.get("/status")
async def get_shiprocket_status():
    """Get Shiprocket connection status"""
    try:
        is_connected = await shiprocket_client.test_connection()
        
        return {
            "platform": "shiprocket",
            "connected": is_connected,
            "currency": "INR",
            "last_check": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Shiprocket status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.post("/sync")
async def sync_shiprocket_data(request: SyncRequest, background_tasks: BackgroundTasks):
    """Trigger Shiprocket data synchronization"""
    try:
        # Log sync start
        await log_sync_operation("shiprocket", "started", {"force_refresh": request.force_refresh})
        
        # Add background task for data sync
        background_tasks.add_task(
            sync_shiprocket_background,
            force_refresh=request.force_refresh,
            limit=request.limit
        )
        
        return {
            "message": "Shiprocket data sync initiated",
            "status": "processing",
            "platform": "shiprocket"
        }
        
    except Exception as e:
        logger.error(f"Shiprocket sync failed: {e}")
        await log_sync_operation("shiprocket", "failed", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

async def sync_shiprocket_background(force_refresh: bool = False, limit: int = 100):
    """Background task for Shiprocket data sync"""
    try:
        logger.info("🔄 Starting Shiprocket background sync")
        
        # Get shipments
        shipments = await shiprocket_client.get_shipments(limit=limit)
        logger.info(f"Retrieved {len(shipments)} Shiprocket shipments")
        
        # Update sync time
        await update_platform_sync_time("shiprocket")
        
        # Log success
        await log_sync_operation("shiprocket", "completed", {
            "shipments_count": len(shipments)
        })
        
        logger.info("✅ Shiprocket background sync completed")
        
    except Exception as e:
        logger.error(f"❌ Shiprocket background sync failed: {e}")
        await log_sync_operation("shiprocket", "failed", {"error": str(e)})

@router.get("/shipments")
async def get_shiprocket_shipments(limit: int = 50, page: int = 1):
    """Get Shiprocket shipments"""
    try:
        shipments = await shiprocket_client.get_shipments(limit=limit, page=page)
        
        # Ensure all costs are in INR
        processed_shipments = []
        for shipment in shipments:
            processed_shipment = {
                **shipment,
                "currency_display": "INR",
                "shipping_charges_inr": float(shipment.get("shipping_charges", 0)),
                "cod_charges_inr": float(shipment.get("cod_charges", 0))
            }
            processed_shipments.append(processed_shipment)
        
        return {
            "shipments": processed_shipments,
            "count": len(processed_shipments),
            "page": page,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get shipments failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get shipments failed: {str(e)}")

@router.get("/tracking/{awb}")
async def get_shipment_tracking(awb: str):
    """Get tracking information for a shipment"""
    try:
        tracking_info = await shiprocket_client.get_tracking_info(awb)
        
        return {
            "awb": awb,
            "tracking_info": tracking_info,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get tracking failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get tracking failed: {str(e)}")

@router.get("/analytics")
async def get_shiprocket_analytics(date_range: str = "last_30_days"):
    """Get Shiprocket analytics summary"""
    try:
        analytics = await shiprocket_client.get_analytics_summary(date_range)
        
        # Ensure all amounts are in INR
        if analytics:
            analytics["currency"] = "INR"
            analytics["total_shipping_cost_inr"] = analytics.get("total_shipping_cost", 0)
            analytics["total_cod_charges_inr"] = analytics.get("total_cod_charges", 0)
            analytics["avg_shipping_cost_inr"] = analytics.get("avg_shipping_cost", 0)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Get analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get analytics failed: {str(e)}")

@router.get("/performance")
async def get_shiprocket_performance():
    """Get Shiprocket delivery performance metrics"""
    try:
        analytics = await shiprocket_client.get_analytics_summary()
        
        # Extract performance metrics
        performance_data = {
            "on_time_delivery_rate": analytics.get("on_time_delivery_rate", 0),
            "avg_delivery_time": analytics.get("avg_delivery_time", 0),
            "total_shipments": analytics.get("total_shipments", 0),
            "delivered_shipments": analytics.get("delivered_shipments", 0),
            "in_transit_shipments": analytics.get("in_transit_shipments", 0),
            "currency": "INR"
        }
        
        return performance_data
        
    except Exception as e:
        logger.error(f"Get performance failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get performance failed: {str(e)}")

@router.get("/costs")
async def get_shiprocket_costs():
    """Get Shiprocket cost breakdown"""
    try:
        analytics = await shiprocket_client.get_analytics_summary()
        
        # Extract cost metrics
        cost_data = {
            "total_shipping_cost": analytics.get("total_shipping_cost", 0),
            "total_cod_charges": analytics.get("total_cod_charges", 0),
            "avg_shipping_cost": analytics.get("avg_shipping_cost", 0),
            "cost_per_shipment": analytics.get("avg_shipping_cost", 0),
            "currency": "INR"
        }
        
        return cost_data
        
    except Exception as e:
        logger.error(f"Get costs failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get costs failed: {str(e)}")

@router.get("/test-connection")
async def test_shiprocket_connection():
    """Test Shiprocket API connection"""
    try:
        is_connected = await shiprocket_client.test_connection()
        
        return {
            "platform": "shiprocket",
            "connected": is_connected,
            "message": "Connection successful" if is_connected else "Connection failed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")