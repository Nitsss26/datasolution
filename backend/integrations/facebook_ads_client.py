import requests
from datetime import datetime, timedelta

class FacebookAdsClient:
    def __init__(self, credentials):
        self.access_token = credentials["access_token"]
        self.ad_account_id = credentials["ad_account_id"]
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def test_connection(self):
        """Test Facebook Ads connection"""
        try:
            url = f"{self.base_url}/me"
            params = {"access_token": self.access_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Facebook Ads connection failed: {str(e)}")
    
    async def fetch_data(self, days=30):
        """Fetch Facebook Ads data"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for Facebook API
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Fetch ad insights
        url = f"{self.base_url}/act_{self.ad_account_id}/insights"
        params = {
            "access_token": self.access_token,
            "time_range": f"{{'since':'{start_date_str}','until':'{end_date_str}'}}",
            "fields": "impressions,clicks,spend,reach,actions,cost_per_action_type",
            "level": "account"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Parse metrics
        insights = data.get("data", [])
        total_spend = sum(float(insight.get("spend", 0)) for insight in insights)
        total_impressions = sum(int(insight.get("impressions", 0)) for insight in insights)
        total_clicks = sum(int(insight.get("clicks", 0)) for insight in insights)
        total_reach = sum(int(insight.get("reach", 0)) for insight in insights)
        
        # Calculate derived metrics
        cpc = total_spend / total_clicks if total_clicks > 0 else 0
        ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
        
        # Mock conversions and revenue for ROAS calculation
        total_conversions = total_clicks * 0.02  # 2% conversion rate
        total_revenue = total_conversions * 50  # $50 per conversion
        roas = total_revenue / total_spend if total_spend > 0 else 0
        
        metrics = {
            "ad_spend": total_spend,
            "impressions": total_impressions,
            "clicks": total_clicks,
            "reach": total_reach,
            "cpc": cpc,
            "ctr": ctr,
            "conversions": total_conversions,
            "revenue": total_revenue,
            "roas": roas
        }
        
        return {
            "metrics": metrics,
            "raw_data": {"insights": insights}
        }
