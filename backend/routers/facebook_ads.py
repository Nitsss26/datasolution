from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from integrations.facebook_client import FacebookClient
from database import log_sync_operation, update_platform_sync_time

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize with environment variables or default values
import os
facebook_client = FacebookClient(
    access_token=os.getenv("FACEBOOK_ACCESS_TOKEN", "demo-token"),
    ad_account_id=os.getenv("FACEBOOK_AD_ACCOUNT_ID", "demo-account")
)

class SyncRequest(BaseModel):
    force_refresh: bool = False
    date_range: Optional[str] = "last_30_days"

@router.get("/status")
async def get_facebook_status():
    """Get Facebook Ads connection status"""
    try:
        is_connected = await facebook_client.test_connection()
        ad_accounts = await facebook_client.get_ad_accounts() if is_connected else []
        
        return {
            "platform": "facebook_ads",
            "connected": is_connected,
            "ad_accounts": ad_accounts,
            "currency": "INR",
            "last_check": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Facebook status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.post("/sync")
async def sync_facebook_data(request: SyncRequest, background_tasks: BackgroundTasks):
    """Trigger Facebook Ads data synchronization"""
    try:
        # Log sync start
        await log_sync_operation("facebook", "started", {"force_refresh": request.force_refresh})
        
        # Add background task for data sync
        background_tasks.add_task(
            sync_facebook_background,
            force_refresh=request.force_refresh,
            date_range=request.date_range
        )
        
        return {
            "message": "Facebook Ads data sync initiated",
            "status": "processing",
            "platform": "facebook_ads"
        }
        
    except Exception as e:
        logger.error(f"Facebook sync failed: {e}")
        await log_sync_operation("facebook", "failed", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

async def sync_facebook_background(force_refresh: bool = False, date_range: str = "last_30_days"):
    """Background task for Facebook Ads data sync"""
    try:
        logger.info("🔄 Starting Facebook Ads background sync")
        
        # Get ad insights
        insights = await facebook_client.get_ad_insights(date_range=date_range, level="campaign")
        logger.info(f"Retrieved {len(insights)} Facebook ad insights")
        
        # Get campaigns
        campaigns = await facebook_client.get_campaigns()
        logger.info(f"Retrieved {len(campaigns)} Facebook campaigns")
        
        # Update sync time
        await update_platform_sync_time("facebook")
        
        # Log success
        await log_sync_operation("facebook", "completed", {
            "insights_count": len(insights),
            "campaigns_count": len(campaigns)
        })
        
        logger.info("✅ Facebook Ads background sync completed")
        
    except Exception as e:
        logger.error(f"❌ Facebook Ads background sync failed: {e}")
        await log_sync_operation("facebook", "failed", {"error": str(e)})

@router.get("/campaigns")
async def get_facebook_campaigns():
    """Get Facebook Ad campaigns"""
    try:
        campaigns = await facebook_client.get_campaigns()
        
        return {
            "campaigns": campaigns,
            "count": len(campaigns),
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get campaigns failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get campaigns failed: {str(e)}")

@router.get("/insights")
async def get_facebook_insights(date_range: str = "last_30_days", level: str = "campaign"):
    """Get Facebook Ad insights"""
    try:
        insights = await facebook_client.get_ad_insights(date_range=date_range, level=level)
        
        # Convert costs to INR display
        processed_insights = []
        for insight in insights:
            processed_insight = {
                **insight,
                "currency_display": "INR",
                "spend_inr": float(insight.get("spend", 0)),
                "conversion_value_inr": float(insight.get("conversion_value", 0)),
                "cpm_inr": float(insight.get("cpm", 0)),
                "cpc_inr": float(insight.get("cpc", 0))
            }
            processed_insights.append(processed_insight)
        
        return {
            "insights": processed_insights,
            "count": len(processed_insights),
            "date_range": date_range,
            "level": level,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get insights failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get insights failed: {str(e)}")

@router.get("/analytics")
async def get_facebook_analytics(date_range: str = "last_30_days"):
    """Get Facebook Ads analytics summary"""
    try:
        analytics = await facebook_client.get_analytics_summary(date_range)
        
        # Ensure all amounts are in INR
        if analytics:
            analytics["currency"] = "INR"
            analytics["total_spend_inr"] = analytics.get("total_spend", 0)
            analytics["total_conversion_value_inr"] = analytics.get("total_conversion_value", 0)
            analytics["cpc_inr"] = analytics.get("cpc", 0)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Get analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get analytics failed: {str(e)}")

@router.get("/audience-insights")
async def get_facebook_audience_insights():
    """Get Facebook audience insights"""
    try:
        audience_data = await facebook_client.get_audience_insights()
        
        return {
            **audience_data,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get audience insights failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get audience insights failed: {str(e)}")

@router.get("/campaign/{campaign_id}/insights")
async def get_campaign_insights(campaign_id: str, date_range: str = "last_30_days"):
    """Get insights for a specific campaign"""
    try:
        insights = await facebook_client.get_campaign_insights(campaign_id, date_range)
        
        # Add INR formatting
        if insights:
            insights["currency_display"] = "INR"
            insights["spend_inr"] = float(insights.get("spend", 0))
            insights["conversion_values_inr"] = float(insights.get("conversion_values", 0))
            insights["cpm_inr"] = float(insights.get("cpm", 0))
            insights["cpc_inr"] = float(insights.get("cpc", 0))
        
        return {
            "campaign_id": campaign_id,
            "insights": insights,
            "date_range": date_range,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get campaign insights failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get campaign insights failed: {str(e)}")

@router.get("/test-connection")
async def test_facebook_connection():
    """Test Facebook Ads API connection"""
    try:
        is_connected = await facebook_client.test_connection()
        
        return {
            "platform": "facebook_ads",
            "connected": is_connected,
            "message": "Connection successful" if is_connected else "Connection failed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")