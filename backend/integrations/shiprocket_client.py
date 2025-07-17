import requests
from typing import Dict, List, Any, Optional
import os

class ShiprocketClient:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.base_url = "https://apiv2.shiprocket.in/v1/external"
        self.token = None
    
    async def _authenticate(self) -> str:
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
    
    async def get_orders(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch orders from Shiprocket"""
        try:
            if not self.token:
                await self._authenticate()
            
            url = f"{self.base_url}/orders"
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {"per_page": limit}
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching Shiprocket orders: {e}")
            return []
    
    async def get_shipments(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch shipments from Shiprocket"""
        try:
            if not self.token:
                await self._authenticate()
            
            url = f"{self.base_url}/shipments"
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {"per_page": limit}
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error fetching Shiprocket shipments: {e}")
            return []
    
    async def track_shipment(self, awb_code: str) -> Dict[str, Any]:
        """Track a specific shipment"""
        try:
            if not self.token:
                await self._authenticate()
            
            url = f"{self.base_url}/courier/track/awb/{awb_code}"
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error tracking Shiprocket shipment: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """Test Shiprocket API connection"""
        try:
            # Test authentication
            url = f"{self.base_url}/auth/login"
            data = {"email": self.email, "password": self.password}
            response = requests.post(url, json=data)
            return response.status_code == 200
        except:
            return False
