import requests
from typing import Dict, Any, List
import os

class FacebookAdsClient:
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def test_connection(self) -> bool:
        """Test Facebook Ads connection"""
        try:
            response = requests.get(
                f"{self.base_url}/me",
                params={"access_token": self.access_token}
            )
            return response.status_code == 200
        except:
            return False
    
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Get campaigns"""
        try:
            response = requests.get(
                f"{self.base_url}/act_{self.ad_account_id}/campaigns",
                params={
                    "access_token": self.access_token,
                    "fields": "id,name,status,objective"
                }
            )
            if response.status_code == 200:
                return response.json().get("data", [])
            return []
        except:
            return []
    
    async def get_insights(self) -> Dict[str, Any]:
        """Get ad insights"""
        try:
            response = requests.get(
                f"{self.base_url}/act_{self.ad_account_id}/insights",
                params={
                    "access_token": self.access_token,
                    "fields": "spend,impressions,clicks,ctr,cpc,cpm",
                    "time_range": '{"since":"2024-01-01","until":"2024-12-31"}'
                }
            )
            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    insight = data[0]
                    return {
                        "spend": float(insight.get("spend", 0)),
                        "impressions": int(insight.get("impressions", 0)),
                        "clicks": int(insight.get("clicks", 0)),
                        "ctr": float(insight.get("ctr", 0)),
                        "cpc": float(insight.get("cpc", 0)),
                        "cpm": float(insight.get("cpm", 0))
                    }
            return {}
        except:
            return {}
