import asyncio
import aiohttp
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from utils.bigquery_client import BigQueryClient

logger = logging.getLogger(__name__)

class FacebookClient:
    def __init__(self, access_token: str = None, ad_account_id: str = None, api_version: str = "v18.0"):
        # Get credentials from environment if not provided
        self.access_token = access_token or os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.ad_account_id = ad_account_id or os.getenv("FACEBOOK_AD_ACCOUNT_ID")
        self.api_version = api_version
        
        # Check if we have required credentials
        if not self.access_token or not self.ad_account_id:
            logger.info("🔄 Running in demo mode - Facebook credentials not found")
            self.is_connected = False
            self.base_url = None
        else:
            self.ad_account_id = self.ad_account_id.replace('act_', '')
            self.base_url = f"https://graph.facebook.com/{api_version}"
            self.is_connected = True
            logger.info(f"✅ Facebook client initialized for account: {self.ad_account_id}")
        
        self.bigquery_client = BigQueryClient()
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Facebook Ads API connection"""
        if not self.is_connected:
            return {"success": False, "error": "Facebook client not initialized - running in demo mode"}
            
        try:
            params = {
                "access_token": self.access_token,
                "fields": "name,account_status,currency,timezone_name"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/act_{self.ad_account_id}",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "message": "Facebook Ads connection successful",
                            "account_name": data.get("name"),
                            "account_status": data.get("account_status"),
                            "currency": data.get("currency"),
                            "timezone": data.get("timezone_name")
                        }
                    else:
                        error_data = await response.json()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_data.get('error', {}).get('message', 'Unknown error')}"
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_campaigns(self, limit: int = 100, date_range: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Get campaigns from Facebook Ads"""
        if not self.is_connected:
            logger.info("🔄 Skipping Facebook campaigns fetch - running in demo mode")
            return []
            
        try:
            # Set default date range (last 30 days)
            if not date_range:
                end_date = datetime.utcnow().date()
                start_date = end_date - timedelta(days=30)
                date_range = {
                    "since": start_date.strftime("%Y-%m-%d"),
                    "until": end_date.strftime("%Y-%m-%d")
                }
            
            fields = [
                "campaign_id",
                "campaign_name",
                "account_id",
                "impressions",
                "clicks",
                "spend",
                "reach",
                "frequency",
                "cpm",
                "cpc",
                "ctr",
                "conversions",
                "conversion_values",
                "cost_per_conversion",
                "objective",
                "status"
            ]
            
            params = {
                "access_token": self.access_token,
                "fields": ",".join(fields),
                "time_range": json.dumps(date_range),
                "limit": limit,
                "level": "campaign"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/act_{self.ad_account_id}/insights",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        campaigns = data.get("data", [])
                        
                        # Process campaigns for BigQuery
                        processed_campaigns = []
                        for campaign in campaigns:
                            processed_campaign = self._process_campaign(campaign, date_range)
                            processed_campaigns.append(processed_campaign)
                        
                        return processed_campaigns
                    else:
                        logger.error(f"Failed to get campaigns: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting campaigns: {e}")
            return []
    
    async def get_ad_sets(self, campaign_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get ad sets for a specific campaign"""
        try:
            fields = [
                "adset_id",
                "adset_name",
                "campaign_id",
                "impressions",
                "clicks",
                "spend",
                "reach",
                "cpm",
                "cpc",
                "ctr",
                "conversions",
                "cost_per_conversion",
                "status"
            ]
            
            params = {
                "access_token": self.access_token,
                "fields": ",".join(fields),
                "limit": limit,
                "level": "adset"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/{campaign_id}/insights",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        logger.error(f"Failed to get ad sets: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting ad sets: {e}")
            return []
    
    async def get_ads(self, adset_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get ads for a specific ad set"""
        try:
            fields = [
                "ad_id",
                "ad_name",
                "adset_id",
                "campaign_id",
                "impressions",
                "clicks",
                "spend",
                "reach",
                "cpm",
                "cpc",
                "ctr",
                "conversions",
                "cost_per_conversion",
                "status"
            ]
            
            params = {
                "access_token": self.access_token,
                "fields": ",".join(fields),
                "limit": limit,
                "level": "ad"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/{adset_id}/insights",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        logger.error(f"Failed to get ads: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting ads: {e}")
            return []
    
    async def sync_to_bigquery(self, force_refresh: bool = False, date_range: Optional[Dict[str, str]] = None):
        """Sync all Facebook Ads data to BigQuery"""
        try:
            logger.info("🔄 Starting Facebook Ads data sync to BigQuery...")
            
            # Determine date range for sync
            if not date_range:
                if force_refresh:
                    # Get last 90 days for full refresh
                    end_date = datetime.utcnow().date()
                    start_date = end_date - timedelta(days=90)
                else:
                    # Get last 7 days for incremental sync
                    end_date = datetime.utcnow().date()
                    start_date = end_date - timedelta(days=7)
                
                date_range = {
                    "since": start_date.strftime("%Y-%m-%d"),
                    "until": end_date.strftime("%Y-%m-%d")
                }
            
            # Sync campaigns
            await self._sync_campaigns_to_bigquery(date_range)
            
            logger.info("✅ Facebook Ads data sync completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Facebook Ads sync failed: {e}")
            raise e
    
    async def _sync_campaigns_to_bigquery(self, date_range: Dict[str, str]):
        """Sync campaigns to BigQuery"""
        try:
            all_campaigns = []
            
            # Get campaigns in batches
            campaigns = await self.get_campaigns(limit=100, date_range=date_range)
            all_campaigns.extend(campaigns)
            
            # Rate limiting
            await asyncio.sleep(1)
            
            if all_campaigns:
                await self.bigquery_client.insert_data("facebook_campaigns", all_campaigns)
                logger.info(f"✅ Synced {len(all_campaigns)} Facebook campaigns to BigQuery")
            
        except Exception as e:
            logger.error(f"❌ Failed to sync Facebook campaigns: {e}")
            raise e
    
    def _process_campaign(self, campaign: Dict[str, Any], date_range: Dict[str, str]) -> Dict[str, Any]:
        """Process campaign data for BigQuery"""
        # Calculate ROAS
        spend = float(campaign.get("spend", 0))
        conversion_value = float(campaign.get("conversion_values", [{}])[0].get("value", 0)) if campaign.get("conversion_values") else 0
        roas = (conversion_value / spend) if spend > 0 else 0
        
        # Calculate cost per conversion
        conversions = float(campaign.get("conversions", [{}])[0].get("value", 0)) if campaign.get("conversions") else 0
        cost_per_conversion = (spend / conversions) if conversions > 0 else 0
        
        return {
            "campaign_id": str(campaign.get("campaign_id")),
            "campaign_name": campaign.get("campaign_name"),
            "account_id": str(campaign.get("account_id")),
            "date_start": date_range.get("since"),
            "date_stop": date_range.get("until"),
            "impressions": int(campaign.get("impressions", 0)),
            "clicks": int(campaign.get("clicks", 0)),
            "spend": spend,
            "reach": int(campaign.get("reach", 0)),
            "frequency": float(campaign.get("frequency", 0)),
            "cpm": float(campaign.get("cpm", 0)),
            "cpc": float(campaign.get("cpc", 0)),
            "ctr": float(campaign.get("ctr", 0)),
            "conversions": int(conversions),
            "conversion_value": conversion_value,
            "cost_per_conversion": cost_per_conversion,
            "roas": roas,
            "objective": campaign.get("objective"),
            "status": campaign.get("status"),
            "platform": "facebook"
        }