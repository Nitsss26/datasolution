import requests
from typing import Dict, Any, List
import os

class ShiprocketClient:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.base_url = "https://apiv2.shiprocket.in/v1/external"
        self.token = None
    
    async def authenticate(self) -> bool:
        """Authenticate with Shiprocket"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": self.email, "password": self.password}
            )
            if response.status_code == 200:
                self.token = response.json().get("token")
                return True
            return False
        except:
            return False
    
    async def test_connection(self) -> bool:
        """Test Shiprocket connection"""
        return await self.authenticate()
    
    async def get_orders(self) -> List[Dict[str, Any]]:
        """Get shipping orders"""
        if not self.token:
            await self.authenticate()
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/orders", headers=headers)
            if response.status_code == 200:
                return response.json().get("data", [])
            return []
        except:
            return []
    
    async def get_shipping_metrics(self) -> Dict[str, Any]:
        """Get shipping metrics"""
        orders = await self.get_orders()
        
        total_shipments = len(orders)
        delivered = sum(1 for order in orders if order.get("status") == "DELIVERED")
        in_transit = sum(1 for order in orders if order.get("status") == "IN_TRANSIT")
        
        return {
            "total_shipments": total_shipments,
            "delivered": delivered,
            "in_transit": in_transit,
            "delivery_rate": round((delivered / total_shipments * 100) if total_shipments > 0 else 0, 2)
        }
