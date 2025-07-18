from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from integrations.google_ads_client import GoogleAdsClient
from database import log_sync_operation, update_platform_sync_time

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize with environment variables or default values
import os
google_ads_client = GoogleAdsClient(
    developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "demo-token"),
    client_id=os.getenv("GOOGLE_ADS_CLIENT_ID", "demo-client-id"),
    client_secret=os.getenv("GOOGLE_ADS_CLIENT_SECRET", "demo-client-secret"),
    refresh_token=os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "demo-refresh-token"),
    customer_id=os.getenv("GOOGLE_ADS_CUSTOMER_ID", "demo-customer")
)

class SyncRequest(BaseModel):
    force_refresh: bool = False
    date_range: Optional[str] = "LAST_30_DAYS"

@router.get("/status")
async def get_google_ads_status():
    """Get Google Ads connection status"""
    try:
        is_connected = await google_ads_client.test_connection()
        account_info = await google_ads_client.get_account_info() if is_connected else None
        
        return {
            "platform": "google_ads",
            "connected": is_connected,
            "account_info": account_info,
            "currency": "INR",
            "last_check": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Google Ads status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.post("/sync")
async def sync_google_ads_data(request: SyncRequest, background_tasks: BackgroundTasks):
    """Trigger Google Ads data synchronization"""
    try:
        # Log sync start
        await log_sync_operation("google_ads", "started", {"force_refresh": request.force_refresh})
        
        # Add background task for data sync
        background_tasks.add_task(
            sync_google_ads_background,
            force_refresh=request.force_refresh,
            date_range=request.date_range
        )
        
        return {
            "message": "Google Ads data sync initiated",
            "status": "processing",
            "platform": "google_ads"
        }
        
    except Exception as e:
        logger.error(f"Google Ads sync failed: {e}")
        await log_sync_operation("google_ads", "failed", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

async def sync_google_ads_background(force_refresh: bool = False, date_range: str = "LAST_30_DAYS"):
    """Background task for Google Ads data sync"""
    try:
        logger.info("🔄 Starting Google Ads background sync")
        
        # Get campaign performance
        campaigns = await google_ads_client.get_campaign_performance(date_range)
        logger.info(f"Retrieved {len(campaigns)} Google Ads campaigns")
        
        # Get keywords performance
        keywords = await google_ads_client.get_keywords_performance()
        logger.info(f"Retrieved {len(keywords)} Google Ads keywords")
        
        # Update sync time
        await update_platform_sync_time("google_ads")
        
        # Log success
        await log_sync_operation("google_ads", "completed", {
            "campaigns_count": len(campaigns),
            "keywords_count": len(keywords)
        })
        
        logger.info("✅ Google Ads background sync completed")
        
    except Exception as e:
        logger.error(f"❌ Google Ads background sync failed: {e}")
        await log_sync_operation("google_ads", "failed", {"error": str(e)})

@router.get("/campaigns")
async def get_google_ads_campaigns(date_range: str = "LAST_30_DAYS"):
    """Get Google Ads campaigns performance"""
    try:
        campaigns = await google_ads_client.get_campaign_performance(date_range)
        
        # Convert costs to INR display
        processed_campaigns = []
        for campaign in campaigns:
            processed_campaign = {
                **campaign,
                "currency_display": "INR",
                "cost_inr": float(campaign.get("cost", 0)),
                "conversion_value_inr": float(campaign.get("conversion_value", 0)),
                "avg_cpc_inr": float(campaign.get("avg_cpc", 0))
            }
            processed_campaigns.append(processed_campaign)
        
        return {
            "campaigns": processed_campaigns,
            "count": len(processed_campaigns),
            "date_range": date_range,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get campaigns failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get campaigns failed: {str(e)}")

@router.get("/keywords")
async def get_google_ads_keywords(campaign_id: Optional[str] = None):
    """Get Google Ads keywords performance"""
    try:
        keywords = await google_ads_client.get_keywords_performance(campaign_id)
        
        # Convert costs to INR display
        processed_keywords = []
        for keyword in keywords:
            processed_keyword = {
                **keyword,
                "currency_display": "INR",
                "cost_inr": float(keyword.get("cost", 0)),
                "avg_cpc_inr": float(keyword.get("avg_cpc", 0))
            }
            processed_keywords.append(processed_keyword)
        
        return {
            "keywords": processed_keywords,
            "count": len(processed_keywords),
            "campaign_id": campaign_id,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get keywords failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get keywords failed: {str(e)}")

@router.get("/analytics")
async def get_google_ads_analytics(date_range: str = "LAST_30_DAYS"):
    """Get Google Ads analytics summary"""
    try:
        analytics = await google_ads_client.get_analytics_summary(date_range)
        
        # Ensure all amounts are in INR
        if analytics:
            analytics["currency"] = "INR"
            analytics["total_cost_inr"] = analytics.get("total_cost", 0)
            analytics["total_conversion_value_inr"] = analytics.get("total_conversion_value", 0)
            analytics["avg_cpc_inr"] = analytics.get("avg_cpc", 0)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Get analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get analytics failed: {str(e)}")

@router.get("/account-info")
async def get_google_ads_account_info():
    """Get Google Ads account information"""
    try:
        account_info = await google_ads_client.get_account_info()
        
        return {
            "account_info": account_info,
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get account info failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get account info failed: {str(e)}")

@router.get("/test-connection")
async def test_google_ads_connection():
    """Test Google Ads API connection"""
    try:
        is_connected = await google_ads_client.test_connection()
        
        return {
            "platform": "google_ads",
            "connected": is_connected,
            "message": "Connection successful" if is_connected else "Connection failed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")