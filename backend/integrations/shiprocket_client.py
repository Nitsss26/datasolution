import requests
from datetime import datetime, timedelta

class ShiprocketClient:
    def __init__(self, credentials):
        self.email = credentials["email"]
        self.password = credentials["password"]
        self.base_url = "https://apiv2.shiprocket.in/v1/external"
        self.token = None
    
    async def authenticate(self):
        """Authenticate with Shiprocket"""
        auth_url = f"{self.base_url}/auth/login"
        auth_data = {
            "email": self.email,
            "password": self.password
        }
        
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
    
    async def test_connection(self):
        """Test Shiprocket connection"""
        try:
            await self.authenticate()
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Shiprocket connection failed: {str(e)}")
    
    async def fetch_data(self, days=30):
        """Fetch Shiprocket data"""
        if not self.token:
            await self.authenticate()
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Fetch orders
        orders_url = f"{self.base_url}/orders"
        orders_response = requests.get(orders_url, headers=headers)
        orders_response.raise_for_status()
        orders_data = orders_response.json()
        
        # Fetch shipments
        shipments_url = f"{self.base_url}/shipments"
        shipments_response = requests.get(shipments_url, headers=headers)
        shipments_response.raise_for_status()
        shipments_data = shipments_response.json()
        
        # Calculate metrics
        orders = orders_data.get("data", [])
        shipments = shipments_data.get("data", [])
        
        total_orders = len(orders)
        total_shipments = len(shipments)
        total_shipping_cost = sum(float(shipment.get("freight", 0)) for shipment in shipments)
        
        # Calculate average delivery time (mock)
        avg_delivery_time = 3.5  # days
        
        # Calculate return rate (mock)
        return_rate = 5.2  # percentage
        
        metrics = {
            "total_orders": total_orders,
            "total_shipments": total_shipments,
            "shipping_cost": total_shipping_cost,
            "avg_delivery_time": avg_delivery_time,
            "return_rate": return_rate,
            "cost_per_order": total_shipping_cost / total_orders if total_orders > 0 else 0
        }
        
        return {
            "metrics": metrics,
            "raw_data": {
                "orders": orders,
                "shipments": shipments
            }
        }
