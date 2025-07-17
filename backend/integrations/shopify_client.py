import requests
from datetime import datetime, timedelta
import asyncio

class ShopifyClient:
    def __init__(self, credentials):
        self.shop_url = credentials["shop_url"]
        self.access_token = credentials["access_token"]
        self.base_url = f"https://{self.shop_url}.myshopify.com/admin/api/2023-10"
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    async def test_connection(self):
        """Test Shopify connection"""
        try:
            response = requests.get(f"{self.base_url}/shop.json", headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Shopify connection failed: {str(e)}")
    
    async def fetch_data(self, days=30):
        """Fetch Shopify data for analytics"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for Shopify API
        start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S%z")
        end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%S%z")
        
        # Fetch orders
        orders_url = f"{self.base_url}/orders.json"
        orders_params = {
            "created_at_min": start_date_str,
            "created_at_max": end_date_str,
            "status": "any",
            "limit": 250
        }
        
        orders_response = requests.get(orders_url, headers=self.headers, params=orders_params)
        orders_response.raise_for_status()
        orders_data = orders_response.json()
        
        # Fetch products
        products_url = f"{self.base_url}/products.json"
        products_response = requests.get(products_url, headers=self.headers)
        products_response.raise_for_status()
        products_data = products_response.json()
        
        # Calculate metrics
        orders = orders_data.get("orders", [])
        total_revenue = sum(float(order.get("total_price", 0)) for order in orders)
        total_orders = len(orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Mock some additional metrics
        total_sessions = total_orders * 15  # Assume 15 sessions per order
        conversion_rate = (total_orders / total_sessions) * 100 if total_sessions > 0 else 0
        
        metrics = {
            "revenue": total_revenue,
            "orders": total_orders,
            "avg_order_value": avg_order_value,
            "sessions": total_sessions,
            "conversion_rate": conversion_rate,
            "products_count": len(products_data.get("products", [])),
            "clicks": total_sessions  # Mock clicks
        }
        
        return {
            "metrics": metrics,
            "raw_data": {
                "orders": orders,
                "products": products_data.get("products", [])
            }
        }
