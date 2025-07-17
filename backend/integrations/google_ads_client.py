import httpx
from typing import Dict, List, Any
from datetime import datetime, timedelta

class GoogleAdsClient:
    def __init__(self, access_token: str, config: Dict[str, Any]):
        self.access_token = access_token
        self.customer_id = config.get("customer_id")
        self.base_url = "https://googleads.googleapis.com/v14"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "developer-token": config.get("developer_token"),
            "login-customer-id": self.customer_id
        }
    
    async def test_connection(self) -> bool:
        """Test the Google Ads API connection"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/customers/{self.customer_id}",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return True
            except Exception as e:
                raise Exception(f"Google Ads connection failed: {str(e)}")
    
    async def fetch_campaigns(self, days: int = 30) -> List[Dict[str, Any]]:
        """Fetch campaigns from Google Ads"""
        query = f"""
        SELECT 
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.cost_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions
        FROM campaign 
        WHERE segments.date DURING LAST_{days}_DAYS
        """
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/customers/{self.customer_id}/googleAds:search",
                    headers=self.headers,
                    json={"query": query},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Google Ads campaigns: {str(e)}")
    
    async def fetch_keywords(self, days: int = 30) -> List[Dict[str, Any]]:
        """Fetch keyword performance"""
        query = f"""
        SELECT 
            ad_group_criterion.keyword.text,
            metrics.cost_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions
        FROM keyword_view 
        WHERE segments.date DURING LAST_{days}_DAYS
        """
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/customers/{self.customer_id}/googleAds:search",
                    headers=self.headers,
                    json={"query": query},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Google Ads keywords: {str(e)}")
    
    async def fetch_data(self) -> Dict[str, Any]:
        """Fetch all relevant data from Google Ads"""
        try:
            campaigns = await self.fetch_campaigns()
            keywords = await self.fetch_keywords()
            
            return {
                "platform": "google_ads",
                "campaigns": campaigns,
                "keywords": keywords,
                "fetched_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to fetch Google Ads data: {str(e)}")
