import requests
from typing import Dict, Any, List
import os

class ShopifyClient:
    def __init__(self, shop_url: str, access_token: str):
        self.shop_url = shop_url.rstrip('/')
        self.access_token = access_token
        self.base_url = f"{self.shop_url}/admin/api/2023-10"
        self.headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test Shopify connection"""
        try:
            response = requests.get(f"{self.base_url}/shop.json", headers=self.headers)
            return response.status_code == 200
        except:
            return False
    
    async def get_orders(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent orders"""
        try:
            response = requests.get(
                f"{self.base_url}/orders.json",
                headers=self.headers,
                params={"limit": limit, "status": "any"}
            )
            if response.status_code == 200:
                return response.json().get("orders", [])
            return []
        except:
            return []
    
    async def get_products(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get products"""
        try:
            response = requests.get(
                f"{self.base_url}/products.json",
                headers=self.headers,
                params={"limit": limit}
            )
            if response.status_code == 200:
                return response.json().get("products", [])
            return []
        except:
            return []
    
    async def get_analytics(self) -> Dict[str, Any]:
        """Get basic analytics"""
        orders = await self.get_orders(250)
        
        total_revenue = sum(float(order.get("total_price", 0)) for order in orders)
        total_orders = len(orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "avg_order_value": round(avg_order_value, 2)
        }
