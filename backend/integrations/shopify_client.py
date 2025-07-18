import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from utils.bigquery_client import BigQueryClient

logger = logging.getLogger(__name__)

class ShopifyClient:
    def __init__(self, shop_domain: str, access_token: str, api_version: str = "2023-10"):
        self.shop_domain = shop_domain.replace('.myshopify.com', '')
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"https://{self.shop_domain}.myshopify.com/admin/api/{api_version}"
        self.headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }
        self.bigquery_client = BigQueryClient()
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Shopify API connection"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/shop.json",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        shop_info = data.get("shop", {})
                        return {
                            "success": True,
                            "message": "Shopify connection successful",
                            "shop_name": shop_info.get("name"),
                            "domain": shop_info.get("domain"),
                            "currency": shop_info.get("currency"),
                            "timezone": shop_info.get("timezone")
                        }
                    else:
                        error_data = await response.json()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_data.get('errors', 'Unknown error')}"
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_orders(self, limit: int = 250, since_id: str = None, created_at_min: str = None) -> List[Dict[str, Any]]:
        """Get orders from Shopify"""
        try:
            params = {
                "limit": min(limit, 250),
                "status": "any"
            }
            
            if since_id:
                params["since_id"] = since_id
            if created_at_min:
                params["created_at_min"] = created_at_min
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/orders.json",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        orders = data.get("orders", [])
                        
                        # Process orders for BigQuery
                        processed_orders = []
                        for order in orders:
                            processed_order = self._process_order(order)
                            processed_orders.append(processed_order)
                        
                        return processed_orders
                    else:
                        logger.error(f"Failed to get orders: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting orders: {e}")
            return []
    
    async def get_customers(self, limit: int = 250, since_id: str = None) -> List[Dict[str, Any]]:
        """Get customers from Shopify"""
        try:
            params = {"limit": min(limit, 250)}
            if since_id:
                params["since_id"] = since_id
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/customers.json",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        customers = data.get("customers", [])
                        
                        # Process customers for BigQuery
                        processed_customers = []
                        for customer in customers:
                            processed_customer = self._process_customer(customer)
                            processed_customers.append(processed_customer)
                        
                        return processed_customers
                    else:
                        logger.error(f"Failed to get customers: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting customers: {e}")
            return []
    
    async def get_products(self, limit: int = 250, since_id: str = None) -> List[Dict[str, Any]]:
        """Get products from Shopify"""
        try:
            params = {"limit": min(limit, 250)}
            if since_id:
                params["since_id"] = since_id
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/products.json",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        products = data.get("products", [])
                        
                        # Process products for BigQuery
                        processed_products = []
                        for product in products:
                            processed_product = self._process_product(product)
                            processed_products.append(processed_product)
                        
                        return processed_products
                    else:
                        logger.error(f"Failed to get products: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            return []
    
    async def sync_to_bigquery(self, force_refresh: bool = False, date_range: Optional[Dict[str, str]] = None):
        """Sync all Shopify data to BigQuery"""
        try:
            logger.info("🔄 Starting Shopify data sync to BigQuery...")
            
            # Determine date range for sync
            if date_range:
                created_at_min = date_range.get("start_date")
            elif not force_refresh:
                # Get last sync time (last 7 days if no previous sync)
                created_at_min = (datetime.utcnow() - timedelta(days=7)).isoformat()
            else:
                created_at_min = None
            
            # Sync orders
            await self._sync_orders_to_bigquery(created_at_min)
            
            # Sync customers
            await self._sync_customers_to_bigquery()
            
            # Sync products
            await self._sync_products_to_bigquery()
            
            logger.info("✅ Shopify data sync completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Shopify sync failed: {e}")
            raise e
    
    async def _sync_orders_to_bigquery(self, created_at_min: str = None):
        """Sync orders to BigQuery"""
        try:
            all_orders = []
            since_id = None
            
            while True:
                orders = await self.get_orders(
                    limit=250,
                    since_id=since_id,
                    created_at_min=created_at_min
                )
                
                if not orders:
                    break
                
                all_orders.extend(orders)
                since_id = orders[-1]["id"]
                
                # Rate limiting
                await asyncio.sleep(0.5)
                
                # Break if we got less than the limit (last page)
                if len(orders) < 250:
                    break
            
            if all_orders:
                await self.bigquery_client.insert_data("shopify_orders", all_orders)
                logger.info(f"✅ Synced {len(all_orders)} Shopify orders to BigQuery")
            
        except Exception as e:
            logger.error(f"❌ Failed to sync orders: {e}")
            raise e
    
    async def _sync_customers_to_bigquery(self):
        """Sync customers to BigQuery"""
        try:
            all_customers = []
            since_id = None
            
            while True:
                customers = await self.get_customers(limit=250, since_id=since_id)
                
                if not customers:
                    break
                
                all_customers.extend(customers)
                since_id = customers[-1]["id"]
                
                # Rate limiting
                await asyncio.sleep(0.5)
                
                # Break if we got less than the limit (last page)
                if len(customers) < 250:
                    break
            
            if all_customers:
                await self.bigquery_client.insert_data("shopify_customers", all_customers)
                logger.info(f"✅ Synced {len(all_customers)} Shopify customers to BigQuery")
            
        except Exception as e:
            logger.error(f"❌ Failed to sync customers: {e}")
            raise e
    
    async def _sync_products_to_bigquery(self):
        """Sync products to BigQuery"""
        try:
            all_products = []
            since_id = None
            
            while True:
                products = await self.get_products(limit=250, since_id=since_id)
                
                if not products:
                    break
                
                all_products.extend(products)
                since_id = products[-1]["id"]
                
                # Rate limiting
                await asyncio.sleep(0.5)
                
                # Break if we got less than the limit (last page)
                if len(products) < 250:
                    break
            
            if all_products:
                await self.bigquery_client.insert_data("shopify_products", all_products)
                logger.info(f"✅ Synced {len(all_products)} Shopify products to BigQuery")
            
        except Exception as e:
            logger.error(f"❌ Failed to sync products: {e}")
            raise e
    
    def _process_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Process order data for BigQuery"""
        return {
            "id": str(order.get("id")),
            "order_number": str(order.get("order_number")),
            "created_at": order.get("created_at"),
            "updated_at": order.get("updated_at"),
            "total_price": float(order.get("total_price", 0)),
            "subtotal_price": float(order.get("subtotal_price", 0)),
            "total_tax": float(order.get("total_tax", 0)),
            "currency": order.get("currency"),
            "financial_status": order.get("financial_status"),
            "fulfillment_status": order.get("fulfillment_status"),
            "customer_id": str(order.get("customer", {}).get("id")) if order.get("customer") else None,
            "email": order.get("email"),
            "phone": order.get("phone"),
            "billing_address": json.dumps(order.get("billing_address")) if order.get("billing_address") else None,
            "shipping_address": json.dumps(order.get("shipping_address")) if order.get("shipping_address") else None,
            "line_items": json.dumps(order.get("line_items", [])),
            "tags": order.get("tags"),
            "source_name": order.get("source_name"),
            "referring_site": order.get("referring_site"),
            "landing_site": order.get("landing_site"),
            "platform": "shopify"
        }
    
    def _process_customer(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer data for BigQuery"""
        return {
            "id": str(customer.get("id")),
            "email": customer.get("email"),
            "first_name": customer.get("first_name"),
            "last_name": customer.get("last_name"),
            "phone": customer.get("phone"),
            "created_at": customer.get("created_at"),
            "updated_at": customer.get("updated_at"),
            "orders_count": int(customer.get("orders_count", 0)),
            "total_spent": float(customer.get("total_spent", 0)),
            "state": customer.get("state"),
            "tags": customer.get("tags"),
            "accepts_marketing": customer.get("accepts_marketing", False),
            "addresses": json.dumps(customer.get("addresses", [])),
            "default_address": json.dumps(customer.get("default_address")) if customer.get("default_address") else None,
            "platform": "shopify"
        }
    
    def _process_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Process product data for BigQuery"""
        return {
            "id": str(product.get("id")),
            "title": product.get("title"),
            "handle": product.get("handle"),
            "product_type": product.get("product_type"),
            "vendor": product.get("vendor"),
            "created_at": product.get("created_at"),
            "updated_at": product.get("updated_at"),
            "published_at": product.get("published_at"),
            "status": product.get("status"),
            "tags": product.get("tags"),
            "variants": json.dumps(product.get("variants", [])),
            "images": json.dumps(product.get("images", [])),
            "options": json.dumps(product.get("options", [])),
            "platform": "shopify"
        }