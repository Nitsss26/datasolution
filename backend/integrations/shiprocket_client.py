import httpx
from typing import Dict, List, Any
from datetime import datetime, timedelta

class ShiprocketClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://apiv2.shiprocket.in/v1/external"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test the Shiprocket API connection"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/orders",
                    headers=self.headers,
                    params={"per_page": 1},
                    timeout=10.0
                )
                response.raise_for_status()
                return True
            except Exception as e:
                raise Exception(f"Shiprocket connection failed: {str(e)}")
    
    async def fetch_orders(self, days: int = 30) -> List[Dict[str, Any]]:
        """Fetch shipping orders from Shiprocket"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/orders",
                    headers=self.headers,
                    params={
                        "per_page": 100,
                        "page": 1
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Shiprocket orders: {str(e)}")
    
    async def fetch_tracking_data(self, order_id: str) -> Dict[str, Any]:
        """Fetch tracking data for a specific order"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/courier/track/awb/{order_id}",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                raise Exception(f"Failed to fetch tracking data: {str(e)}")
    
    async def fetch_shipping_rates(self) -> List[Dict[str, Any]]:
        """Fetch available shipping rates"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/courier/serviceability",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
            except Exception as e:
                raise Exception(f"Failed to fetch shipping rates: {str(e)}")
    
    async def fetch_data(self) -> Dict[str, Any]:
        """Fetch all relevant data from Shiprocket"""
        try:
            orders = await self.fetch_orders()
            
            return {
                "platform": "shiprocket",
                "orders": orders,
                "fetched_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to fetch Shiprocket data: {str(e)}")
