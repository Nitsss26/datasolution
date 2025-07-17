import httpx
from typing import Dict, List, Any
from datetime import datetime, timedelta

class FacebookAdsClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test the Facebook Ads API connection"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/me",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return True
            except Exception as e:
                raise Exception(f"Facebook Ads connection failed: {str(e)}")
    
    async def fetch_ad_accounts(self) -> List[Dict[str, Any]]:
        """Fetch ad accounts"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/me/adaccounts",
                    headers=self.headers,
                    params={"fields": "id,name,account_status"},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Facebook ad accounts: {str(e)}")
    
    async def fetch_campaigns(self, ad_account_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Fetch campaigns for an ad account"""
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        until_date = datetime.now().strftime("%Y-%m-%d")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/{ad_account_id}/campaigns",
                    headers=self.headers,
                    params={
                        "fields": "id,name,status,spend,impressions,clicks,conversions",
                        "time_range": f"{{'since':'{since_date}','until':'{until_date}'}}"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Facebook campaigns: {str(e)}")
    
    async def fetch_insights(self, ad_account_id: str, days: int = 30) -> Dict[str, Any]:
        """Fetch ad insights"""
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        until_date = datetime.now().strftime("%Y-%m-%d")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/{ad_account_id}/insights",
                    headers=self.headers,
                    params={
                        "fields": "spend,impressions,clicks,conversions,ctr,cpc,cpm,roas",
                        "time_range": f"{{'since':'{since_date}','until':'{until_date}'}}"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Facebook insights: {str(e)}")
    
    async def fetch_data(self) -> Dict[str, Any]:
        """Fetch all relevant data from Facebook Ads"""
        try:
            ad_accounts = await self.fetch_ad_accounts()
            all_campaigns = []
            all_insights = []
            
            for account in ad_accounts:
                account_id = account["id"]
                campaigns = await self.fetch_campaigns(account_id)
                insights = await self.fetch_insights(account_id)
                
                all_campaigns.extend(campaigns)
                all_insights.extend(insights)
            
            return {
                "platform": "facebook_ads",
                "ad_accounts": ad_accounts,
                "campaigns": all_campaigns,
                "insights": all_insights,
                "fetched_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to fetch Facebook Ads data: {str(e)}")
