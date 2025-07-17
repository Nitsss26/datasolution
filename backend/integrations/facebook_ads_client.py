import requests
from typing import Dict, Any, List
import os

class FacebookAdsClient:
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """Fetch campaigns from Facebook Ads"""
        try:
            url = f"{self.base_url}/act_{self.ad_account_id}/campaigns"
            params = {
                "access_token": self.access_token,
                "fields": "id,name,status,objective,created_time,updated_time"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching Facebook campaigns: {e}")
            return []
    
    async def get_insights(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get insights from Facebook Ads"""
        try:
            url = f"{self.base_url}/act_{self.ad_account_id}/insights"
            params = {
                "access_token": self.access_token,
                "time_range": f"{{'since':'{start_date}','until':'{end_date}'}}",
                "fields": "spend,impressions,clicks,ctr,cpc,cpm,reach,frequency,actions"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json().get("data", [])
            if data:
                insight = data[0]
                return {
                    "spend": float(insight.get("spend", 0)),
                    "impressions": int(insight.get("impressions", 0)),
                    "clicks": int(insight.get("clicks", 0)),
                    "ctr": float(insight.get("ctr", 0)),
                    "cpc": float(insight.get("cpc", 0)),
                    "platform": "facebook"
                }
            return {}
        except Exception as e:
            print(f"Error fetching Facebook insights: {e}")
            return {}
