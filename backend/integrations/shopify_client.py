import requests
from typing import Dict, List, Any, Optional
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
    
    async def get_customers(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch customers from Shopify"""
        try:
            url = f"{self.base_url}/customers.json"
            params = {"limit": limit}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            return response.json().get("customers", [])
        except Exception as e:
            print(f"Error fetching Shopify customers: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test Shopify API connection"""
        try:
            url = f"{self.base_url}/shop.json"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False
