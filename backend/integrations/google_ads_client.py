import requests
from datetime import datetime, timedelta

class GoogleAdsClient:
    def __init__(self, credentials):
        self.access_token = credentials["access_token"]
        self.customer_id = credentials["customer_id"]
        self.developer_token = credentials["developer_token"]
        self.base_url = "https://googleads.googleapis.com/v14"
    
    async def test_connection(self):
        """Test Google Ads connection"""
        try:
            url = f"{self.base_url}/customers/{self.customer_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "developer-token": self.developer_token
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Google Ads connection failed: {str(e)}")
    
    async def fetch_data(self, days=30):
        """Fetch Google Ads data"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for Google Ads API
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Search query for campaign performance
        query = f"""
        SELECT 
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign 
        WHERE segments.date >= '{start_date_str}' 
        AND segments.date <= '{end_date_str}'
        """
        
        url = f"{self.base_url}/customers/{self.customer_id}/googleAds:search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "developer-token": self.developer_token,
            "Content-Type": "application/json"
        }
        
        payload = {"query": query}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Parse metrics
        results = data.get("results", [])
        total_impressions = sum(int(result.get("metrics", {}).get("impressions", 0)) for result in results)
        total_clicks = sum(int(result.get("metrics", {}).get("clicks", 0)) for result in results)
        total_cost_micros = sum(int(result.get("metrics", {}).get("costMicros", 0)) for result in results)
        total_conversions = sum(float(result.get("metrics", {}).get("conversions", 0)) for result in results)
        total_conversion_value = sum(float(result.get("metrics", {}).get("conversionsValue", 0)) for result in results)
        
        # Convert micros to actual cost
        total_cost = total_cost_micros / 1000000
        
        # Calculate derived metrics
        cpc = total_cost / total_clicks if total_clicks > 0 else 0
        ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
        cost_per_conversion = total_cost / total_conversions if total_conversions > 0 else 0
        roas = total_conversion_value / total_cost if total_cost > 0 else 0
        
        metrics = {
            "ad_spend": total_cost,
            "impressions": total_impressions,
            "clicks": total_clicks,
            "cpc": cpc,
            "ctr": ctr,
            "conversions": total_conversions,
            "cost_per_conversion": cost_per_conversion,
            "revenue": total_conversion_value,
            "roas": roas
        }
        
        return {
            "metrics": metrics,
            "raw_data": {"results": results}
        }
