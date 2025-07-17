import requests
from typing import Dict, Any, List
import os

class ShopifyClient:
    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain
        self.access_token = access_token
        self.base_url = f"https://{shop_domain}.myshopify.com/admin/api/2023-10"
        self.headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }
    
    async def get_orders(self, limit: int = 50, status: str = "any") -> List[Dict[str, Any]]:
        """Fetch orders from Shopify"""
        try:
            url = f"{self.base_url}/orders.json"
            params = {"limit": limit, "status": status}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json().get("orders", [])
        except Exception as e:
            print(f"Error fetching Shopify orders: {e}")
            return []
    
    async def get_products(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch products from Shopify"""
        try:
            url = f"{self.base_url}/products.json"
            params = {"limit": limit}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json().get("products", [])
        except Exception as e:
            print(f"Error fetching Shopify products: {e}")
            return []
    
    async def get_analytics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get analytics data from Shopify"""
        try:
            # This would typically involve multiple API calls to get comprehensive analytics
            orders = await self.get_orders(limit=250)
            
            total_revenue = sum(float(order.get("total_price", 0)) for order in orders)
            total_orders = len(orders)
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            return {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "average_order_value": avg_order_value,
                "platform": "shopify"
            }
        except Exception as e:
            print(f"Error fetching Shopify analytics: {e}")
            return {}
