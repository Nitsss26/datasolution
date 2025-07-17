import requests
from typing import Dict, List, Any, Optional
import os

class FacebookAdsClient:
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    async def get_campaigns(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch campaigns from Facebook Ads"""
        try:
            url = f"{self.base_url}/act_{self.ad_account_id}/campaigns"
            params = {
                "fields": "id,name,status,objective,created_time,updated_time",
                "limit": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching Facebook campaigns: {e}")
            return []
    
    async def get_campaign_insights(self, campaign_id: str, date_range: str = "last_30d") -> Dict[str, Any]:
        """Fetch campaign performance insights"""
        try:
            url = f"{self.base_url}/{campaign_id}/insights"
            params = {
                "fields": "spend,impressions,clicks,ctr,cpc,cpm,reach,frequency,actions",
                "date_preset": date_range
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json().get("data", [])
            return data[0] if data else {}
        except Exception as e:
            print(f"Error fetching Facebook campaign insights: {e}")
            return {}
    
    async def get_ad_account_insights(self, date_range: str = "last_30d") -> Dict[str, Any]:
        """Fetch ad account level insights"""
        try:
            url = f"{self.base_url}/act_{self.ad_account_id}/insights"
            params = {
                "fields": "spend,impressions,clicks,ctr,cpc,cpm,reach,frequency,actions,action_values",
                "date_preset": date_range
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json().get("data", [])
            return data[0] if data else {}
        except Exception as e:
            print(f"Error fetching Facebook ad account insights: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """Test Facebook Ads API connection"""
        try:
            url = f"{self.base_url}/me"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False
