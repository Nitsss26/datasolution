import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from utils.bigquery_client import BigQueryClient

logger = logging.getLogger(__name__)

class GoogleAdsClient:
    def __init__(self, developer_token: str, client_id: str, client_secret: str, 
                 refresh_token: str, customer_id: str, api_version: str = "v14"):
        self.developer_token = developer_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.customer_id = customer_id.replace('-', '')
        self.api_version = api_version
        self.base_url = f"https://googleads.googleapis.com/{api_version}"
        self.access_token = None
        self.bigquery_client = BigQueryClient()
    
    async def _get_access_token(self) -> str:
        """Get access token using refresh token"""
        try:
            if self.access_token:
                return self.access_token
            
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://oauth2.googleapis.com/token",
                    data=data
                ) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        self.access_token = token_data.get("access_token")
                        return self.access_token
                    else:
                        raise Exception(f"Failed to get access token: HTTP {response.status}")
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            raise e
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Google Ads API connection"""
        try:
            access_token = await self._get_access_token()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "developer-token": self.developer_token,
                "Content-Type": "application/json"
            }
            
            # Test with a simple customer query
            query = "SELECT customer.id, customer.descriptive_name, customer.currency_code FROM customer LIMIT 1"
            
            data = {
                "query": query
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/customers/{self.customer_id}/googleAds:search",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        customer_info = result.get("results", [{}])[0].get("customer", {})
                        return {
                            "success": True,
                            "message": "Google Ads connection successful",
                            "customer_id": customer_info.get("id"),
                            "account_name": customer_info.get("descriptiveName"),
                            "currency": customer_info.get("currencyCode")
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
        """Get campaigns from Google Ads"""
        try:
            access_token = await self._get_access_token()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "developer-token": self.developer_token,
                "Content-Type": "application/json"
            }
            
            # Set default date range (last 30 days)
            if not date_range:
                end_date = datetime.utcnow().date()
                start_date = end_date - timedelta(days=30)
                date_range = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
            
            # Google Ads Query Language (GAQL)
            query = f"""
            SELECT 
                campaign.id,
                campaign.name,
                campaign.status,
                campaign.advertising_channel_type,
                campaign.bidding_strategy_type,
                segments.date,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_per_conversion,
                metrics.value_per_conversion
            FROM campaign 
            WHERE segments.date BETWEEN '{date_range["start_date"]}' AND '{date_range["end_date"]}'
            ORDER BY segments.date DESC
            LIMIT {limit}
            """
            
            data = {"query": query}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/customers/{self.customer_id}/googleAds:search",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        campaigns = result.get("results", [])
                        
                        # Process campaigns for BigQuery
                        processed_campaigns = []
                        for campaign in campaigns:
                            processed_campaign = self._process_campaign(campaign)
                            processed_campaigns.append(processed_campaign)
                        
                        return processed_campaigns
                    else:
                        logger.error(f"Failed to get campaigns: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting campaigns: {e}")
            return []
    
    async def get_keywords(self, campaign_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get keywords for a specific campaign"""
        try:
            access_token = await self._get_access_token()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "developer-token": self.developer_token,
                "Content-Type": "application/json"
            }
            
            query = f"""
            SELECT 
                ad_group_criterion.keyword.text,
                ad_group_criterion.keyword.match_type,
                ad_group.id,
                ad_group.name,
                campaign.id,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc,
                metrics.quality_score
            FROM keyword_view 
            WHERE campaign.id = {campaign_id}
            AND segments.date DURING LAST_30_DAYS
            LIMIT {limit}
            """
            
            data = {"query": query}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/customers/{self.customer_id}/googleAds:search",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("results", [])
                    else:
                        logger.error(f"Failed to get keywords: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting keywords: {e}")
            return []
    
    async def sync_to_bigquery(self, force_refresh: bool = False, date_range: Optional[Dict[str, str]] = None):
        """Sync all Google Ads data to BigQuery"""
        try:
            logger.info("🔄 Starting Google Ads data sync to BigQuery...")
            
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
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
            
            # Sync campaigns
            await self._sync_campaigns_to_bigquery(date_range)
            
            logger.info("✅ Google Ads data sync completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Google Ads sync failed: {e}")
            raise e
    
    async def _sync_campaigns_to_bigquery(self, date_range: Dict[str, str]):
        """Sync campaigns to BigQuery"""
        try:
            all_campaigns = []
            
            # Get campaigns in batches
            campaigns = await self.get_campaigns(limit=1000, date_range=date_range)
            all_campaigns.extend(campaigns)
            
            # Rate limiting
            await asyncio.sleep(1)
            
            if all_campaigns:
                await self.bigquery_client.insert_data("google_campaigns", all_campaigns)
                logger.info(f"✅ Synced {len(all_campaigns)} Google Ads campaigns to BigQuery")
            
        except Exception as e:
            logger.error(f"❌ Failed to sync Google Ads campaigns: {e}")
            raise e
    
    def _process_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process campaign data for BigQuery"""
        campaign = campaign_data.get("campaign", {})
        metrics = campaign_data.get("metrics", {})
        segments = campaign_data.get("segments", {})
        
        # Convert cost from micros to actual currency
        cost_micros = int(metrics.get("costMicros", 0))
        cost = cost_micros / 1000000  # Convert micros to currency units
        
        # Convert average CPC from micros
        avg_cpc_micros = int(metrics.get("averageCpc", 0))
        avg_cpc = avg_cpc_micros / 1000000
        
        # Calculate conversions and values
        conversions = float(metrics.get("conversions", 0))
        conversion_value = float(metrics.get("conversionsValue", 0))
        
        # Calculate cost per conversion
        cost_per_conversion = (cost / conversions) if conversions > 0 else 0
        
        # Calculate value per conversion
        value_per_conversion = (conversion_value / conversions) if conversions > 0 else 0
        
        return {
            "campaign_id": str(campaign.get("id")),
            "campaign_name": campaign.get("name"),
            "customer_id": self.customer_id,
            "date": segments.get("date"),
            "impressions": int(metrics.get("impressions", 0)),
            "clicks": int(metrics.get("clicks", 0)),
            "cost": int(cost_micros),  # Store as micros for precision
            "conversions": conversions,
            "conversion_value": conversion_value,
            "ctr": float(metrics.get("ctr", 0)),
            "average_cpc": int(avg_cpc_micros),  # Store as micros for precision
            "cost_per_conversion": cost_per_conversion,
            "value_per_conversion": value_per_conversion,
            "campaign_status": campaign.get("status"),
            "campaign_type": campaign.get("advertisingChannelType"),
            "bidding_strategy": campaign.get("biddingStrategyType"),
            "platform": "google"
        }