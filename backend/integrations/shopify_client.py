import httpx
import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta

class ShopifyClient:
    def __init__(self, api_key: str, shop_domain: str):
        self.api_key = api_key
        self.shop_domain = shop_domain
        self.base_url = f"https://{shop_domain}.myshopify.com/admin/api/2023-10"
        self.headers = {
            "X-Shopify-Access-Token": api_key,
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test the Shopify API connection"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/shop.json",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return True
            except Exception as e:
                raise Exception(f"Shopify connection failed: {str(e)}")
    
    async def fetch_orders(self, days: int = 30) -> List[Dict[str, Any]]:
        """Fetch orders from Shopify"""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/orders.json",
                    headers=self.headers,
                    params={
                        "status": "any",
                        "created_at_min": since_date,
                        "limit": 250
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("orders", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Shopify orders: {str(e)}")
    
    async def fetch_products(self) -> List[Dict[str, Any]]:
        """Fetch products from Shopify"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/products.json",
                    headers=self.headers,
                    params={"limit": 250},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("products", [])
            except Exception as e:
                raise Exception(f"Failed to fetch Shopify products: {str(e)}")
    
    async def fetch_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Fetch analytics data from Shopify"""
        orders = await self.fetch_orders(days)
        
        # Calculate metrics
        total_revenue = sum(float(order.get("total_price", 0)) for order in orders)
        total_orders = len(orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "average_order_value": avg_order_value,
            "orders": orders
        }
    
    async def fetch_data(self) -> Dict[str, Any]:
        """Fetch all relevant data from Shopify"""
        try:
            orders = await self.fetch_orders()
            products = await self.fetch_products()
            analytics = await self.fetch_analytics()
            
            return {
                "platform": "shopify",
                "orders": orders,
                "products": products,
                "analytics": analytics,
                "fetched_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to fetch Shopify data: {str(e)}")
