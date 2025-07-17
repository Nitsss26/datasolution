import requests
from typing import Dict, Any, List
import os

class ShiprocketClient:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.base_url = "https://apiv2.shiprocket.in/v1/external"
        self.token = None
    
    async def authenticate(self):
        """Authenticate with Shiprocket API"""
        try:
            url = f"{self.base_url}/auth/login"
            data = {
                "email": self.email,
                "password": self.password
            }
            
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            self.token = response.json().get("token")
            return self.token
        except Exception as e:
            print(f"Error authenticating with Shiprocket: {e}")
            return None
    
    async def get_orders(self) -> List[Dict[str, Any]]:
        """Fetch orders from Shiprocket"""
        try:
            if not self.token:
                await self.authenticate()
            
            url = f"{self.base_url}/orders"
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching Shiprocket orders: {e}")
            return []
    
    async def get_tracking_data(self, order_id: str) -> Dict[str, Any]:
        """Get tracking data for an order"""
        try:
            if not self.token:
                await self.authenticate()
            
            url = f"{self.base_url}/courier/track/awb/{order_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error fetching tracking data: {e}")
            return {}
