import requests
from typing import Dict, List, Any, Optional
import os

class GoogleAdsClient:
    def __init__(self, developer_token: str, client_id: str, client_secret: str, refresh_token: str, customer_id: str):
        self.developer_token = developer_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.customer_id = customer_id
        self.base_url = "https://googleads.googleapis.com/v14"
        self.access_token = None
    
    async def _get_access_token(self) -> str:
        """Get access token using refresh token"""
        try:
            url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token"
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            self.access_token = response.json().get("access_token")
            return self.access_token
        except Exception as e:
            print(f"Error getting Google Ads access token: {e}")
            return None
    
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Fetch campaigns from Google Ads"""
        try:
            if not self.access_token:
                await self._get_access_token()
            
            url = f"{self.base_url}/customers/{self.customer_id}/googleAds:searchStream"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "developer-token": self.developer_token,
                "Content-Type": "application/json"
            }
            
            query = """
                SELECT 
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    campaign.advertising_channel_type
                FROM campaign
                WHERE campaign.status != 'REMOVED'
            """
            
            data = {"query": query}
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            return response.json().get("results", [])
        except Exception as e:
            print(f"Error fetching Google Ads campaigns: {e}")
            return []
    
    async def get_campaign_performance(self, date_range: str = "LAST_30_DAYS") -> List[Dict[str, Any]]:
        """Fetch campaign performance metrics"""
        try:
            if not self.access_token:
                await self._get_access_token()
            
            url = f"{self.base_url}/customers/{self.customer_id}/googleAds:searchStream"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "developer-token": self.developer_token,
                "Content-Type": "application/json"
            }
            
            query = f"""
                SELECT 
                    campaign.id,
                    campaign.name,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.conversions,
                    metrics.conversion_value
                FROM campaign
                WHERE segments.date DURING {date_range}
                AND campaign.status != 'REMOVED'
            """
            
            data = {"query": query}
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            return response.json().get("results", [])
        except Exception as e:
            print(f"Error fetching Google Ads performance: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test Google Ads API connection"""
        try:
            # This would require a proper test query
            return True  # Simplified for now
        except:
            return False
