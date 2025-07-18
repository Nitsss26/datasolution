import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from .bigquery_client import BigQueryClient
from ..integrations.shopify_client import ShopifyClient
from ..integrations.facebook_client import FacebookClient
from ..integrations.google_ads_client import GoogleAdsClient
from ..integrations.shiprocket_client import ShiprocketClient

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, bigquery_client: BigQueryClient):
        self.bigquery = bigquery_client
        self.shopify = ShopifyClient()
        self.facebook = FacebookClient()
        self.google_ads = GoogleAdsClient()
        self.shiprocket = ShiprocketClient()
    
    async def sync_all_platforms(self, platforms: List[str], force_refresh: bool = False):
        """Sync data from all specified platforms"""
        try:
            tasks = []
            
            if "all" in platforms or "shopify" in platforms:
                tasks.append(self.sync_shopify_data(force_refresh))
            
            if "all" in platforms or "facebook" in platforms:
                tasks.append(self.sync_facebook_data(force_refresh))
            
            if "all" in platforms or "google" in platforms:
                tasks.append(self.sync_google_ads_data(force_refresh))
            
            if "all" in platforms or "shiprocket" in platforms:
                tasks.append(self.sync_shiprocket_data(force_refresh))
            
            # Execute all sync tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log results
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Sync task {i} failed: {result}")
                else:
                    logger.info(f"Sync task {i} completed successfully")
            
            logger.info("✅ All platform sync completed")
            
        except Exception as e:
            logger.error(f"❌ Platform sync failed: {e}")
            raise e
    
    async def sync_shopify_data(self, force_refresh: bool = False):
        """Sync Shopify data to BigQuery"""
        try:
            logger.info("🔄 Starting Shopify data sync...")
            
            # Get orders
            orders = await self.shopify.get_orders(limit=250)
            if orders:
                processed_orders = self._process_shopify_orders(orders)
                await self.bigquery.insert_data("shopify_orders", processed_orders)
                logger.info(f"✅ Synced {len(processed_orders)} Shopify orders")
            
            # Get customers
            customers = await self.shopify.get_customers(limit=250)
            if customers:
                processed_customers = self._process_shopify_customers(customers)
                await self.bigquery.insert_data("shopify_customers", processed_customers)
                logger.info(f"✅ Synced {len(processed_customers)} Shopify customers")
            
            # Get products
            products = await self.shopify.get_products(limit=250)
            if products:
                processed_products = self._process_shopify_products(products)
                await self.bigquery.insert_data("shopify_products", processed_products)
                logger.info(f"✅ Synced {len(processed_products)} Shopify products")
            
        except Exception as e:
            logger.error(f"❌ Shopify sync failed: {e}")
            raise e
    
    async def sync_facebook_data(self, force_refresh: bool = False):
        """Sync Facebook Ads data to BigQuery"""
        try:
            logger.info("🔄 Starting Facebook Ads data sync...")
            
            # Get ad insights
            insights = await self.facebook.get_ad_insights(
                date_range="last_30_days",
                level="ad"
            )
            
            if insights:
                processed_insights = self._process_facebook_insights(insights)
                await self.bigquery.insert_data("facebook_ads", processed_insights)
                logger.info(f"✅ Synced {len(processed_insights)} Facebook ad insights")
            
        except Exception as e:
            logger.error(f"❌ Facebook sync failed: {e}")
            raise e
    
    async def sync_google_ads_data(self, force_refresh: bool = False):
        """Sync Google Ads data to BigQuery"""
        try:
            logger.info("🔄 Starting Google Ads data sync...")
            
            # Get campaign performance
            campaigns = await self.google_ads.get_campaign_performance(
                date_range="LAST_30_DAYS"
            )
            
            if campaigns:
                processed_campaigns = self._process_google_ads_data(campaigns)
                await self.bigquery.insert_data("google_ads", processed_campaigns)
                logger.info(f"✅ Synced {len(processed_campaigns)} Google Ads campaigns")
            
        except Exception as e:
            logger.error(f"❌ Google Ads sync failed: {e}")
            raise e
    
    async def sync_shiprocket_data(self, force_refresh: bool = False):
        """Sync Shiprocket data to BigQuery"""
        try:
            logger.info("🔄 Starting Shiprocket data sync...")
            
            # Get shipments
            shipments = await self.shiprocket.get_shipments(limit=250)
            
            if shipments:
                processed_shipments = self._process_shiprocket_data(shipments)
                await self.bigquery.insert_data("shiprocket_shipments", processed_shipments)
                logger.info(f"✅ Synced {len(processed_shipments)} Shiprocket shipments")
            
        except Exception as e:
            logger.error(f"❌ Shiprocket sync failed: {e}")
            raise e
    
    async def get_analytics(self, platforms: List[str], time_range: str, metrics: Optional[List[str]] = None, granularity: str = "daily"):
        """Get comprehensive analytics data"""
        try:
            # Get raw data from BigQuery
            raw_data = await self.bigquery.get_analytics_data(platforms, time_range, granularity)
            
            # Process and calculate metrics
            analytics = self._calculate_comprehensive_metrics(raw_data, platforms, time_range)
            
            return analytics
            
        except Exception as e:
            logger.error(f"❌ Analytics calculation failed: {e}")
            raise e
    
    def _process_shopify_orders(self, orders: List[Dict]) -> List[Dict]:
        """Process Shopify orders for BigQuery"""
        processed = []
        
        for order in orders:
            processed_order = {
                "order_id": str(order.get("id")),
                "customer_id": str(order.get("customer", {}).get("id")) if order.get("customer") else None,
                "email": order.get("email"),
                "total_price": float(order.get("total_price", 0)),
                "subtotal_price": float(order.get("subtotal_price", 0)),
                "total_tax": float(order.get("total_tax", 0)),
                "currency": order.get("currency"),
                "financial_status": order.get("financial_status"),
                "fulfillment_status": order.get("fulfillment_status"),
                "created_at": order.get("created_at"),
                "updated_at": order.get("updated_at"),
                "line_items": order.get("line_items", []),
                "shipping_address": order.get("shipping_address"),
                "billing_address": order.get("billing_address")
            }
            processed.append(processed_order)
        
        return processed
    
    def _process_shopify_customers(self, customers: List[Dict]) -> List[Dict]:
        """Process Shopify customers for BigQuery"""
        processed = []
        
        for customer in customers:
            processed_customer = {
                "customer_id": str(customer.get("id")),
                "email": customer.get("email"),
                "first_name": customer.get("first_name"),
                "last_name": customer.get("last_name"),
                "orders_count": int(customer.get("orders_count", 0)),
                "total_spent": float(customer.get("total_spent", 0)),
                "created_at": customer.get("created_at"),
                "updated_at": customer.get("updated_at"),
                "state": customer.get("state"),
                "country": customer.get("default_address", {}).get("country") if customer.get("default_address") else None
            }
            processed.append(processed_customer)
        
        return processed
    
    def _process_shopify_products(self, products: List[Dict]) -> List[Dict]:
        """Process Shopify products for BigQuery"""
        processed = []
        
        for product in products:
            processed_product = {
                "product_id": str(product.get("id")),
                "title": product.get("title"),
                "vendor": product.get("vendor"),
                "product_type": product.get("product_type"),
                "handle": product.get("handle"),
                "status": product.get("status"),
                "created_at": product.get("created_at"),
                "updated_at": product.get("updated_at"),
                "variants": product.get("variants", []),
                "images": product.get("images", [])
            }
            processed.append(processed_product)
        
        return processed
    
    def _process_facebook_insights(self, insights: List[Dict]) -> List[Dict]:
        """Process Facebook ad insights for BigQuery"""
        processed = []
        
        for insight in insights:
            processed_insight = {
                "campaign_id": insight.get("campaign_id"),
                "campaign_name": insight.get("campaign_name"),
                "adset_id": insight.get("adset_id"),
                "adset_name": insight.get("adset_name"),
                "ad_id": insight.get("ad_id"),
                "ad_name": insight.get("ad_name"),
                "date_start": insight.get("date_start"),
                "date_stop": insight.get("date_stop"),
                "impressions": int(insight.get("impressions", 0)),
                "clicks": int(insight.get("clicks", 0)),
                "spend": float(insight.get("spend", 0)),
                "conversions": int(insight.get("conversions", 0)),
                "conversion_value": float(insight.get("conversion_value", 0)),
                "cpm": float(insight.get("cpm", 0)),
                "cpc": float(insight.get("cpc", 0)),
                "ctr": float(insight.get("ctr", 0)),
                "created_at": datetime.utcnow().isoformat()
            }
            processed.append(processed_insight)
        
        return processed
    
    def _process_google_ads_data(self, campaigns: List[Dict]) -> List[Dict]:
        """Process Google Ads data for BigQuery"""
        processed = []
        
        for campaign in campaigns:
            processed_campaign = {
                "campaign_id": campaign.get("campaign_id"),
                "campaign_name": campaign.get("campaign_name"),
                "ad_group_id": campaign.get("ad_group_id"),
                "ad_group_name": campaign.get("ad_group_name"),
                "keyword": campaign.get("keyword"),
                "date": campaign.get("date"),
                "impressions": int(campaign.get("impressions", 0)),
                "clicks": int(campaign.get("clicks", 0)),
                "cost": float(campaign.get("cost", 0)),
                "conversions": float(campaign.get("conversions", 0)),
                "conversion_value": float(campaign.get("conversion_value", 0)),
                "avg_cpc": float(campaign.get("avg_cpc", 0)),
                "ctr": float(campaign.get("ctr", 0)),
                "quality_score": int(campaign.get("quality_score", 0)),
                "created_at": datetime.utcnow().isoformat()
            }
            processed.append(processed_campaign)
        
        return processed
    
    def _process_shiprocket_data(self, shipments: List[Dict]) -> List[Dict]:
        """Process Shiprocket data for BigQuery"""
        processed = []
        
        for shipment in shipments:
            processed_shipment = {
                "shipment_id": str(shipment.get("shipment_id")),
                "order_id": str(shipment.get("order_id")),
                "awb": shipment.get("awb"),
                "courier_name": shipment.get("courier_name"),
                "status": shipment.get("status"),
                "pickup_date": shipment.get("pickup_date"),
                "delivered_date": shipment.get("delivered_date"),
                "weight": float(shipment.get("weight", 0)),
                "length": float(shipment.get("length", 0)),
                "breadth": float(shipment.get("breadth", 0)),
                "height": float(shipment.get("height", 0)),
                "shipping_charges": float(shipment.get("shipping_charges", 0)),
                "cod_charges": float(shipment.get("cod_charges", 0)),
                "pickup_location": shipment.get("pickup_location"),
                "delivery_location": shipment.get("delivery_location"),
                "created_at": datetime.utcnow().isoformat()
            }
            processed.append(processed_shipment)
        
        return processed
    
    def _calculate_comprehensive_metrics(self, raw_data: List[Dict], platforms: List[str], time_range: str) -> Dict[str, Any]:
        """Calculate comprehensive D2C metrics"""
        try:
            if not raw_data:
                return self._get_empty_analytics()
            
            df = pd.DataFrame(raw_data)
            
            # Calculate D2C metrics
            d2c_metrics = self._calculate_d2c_metrics(df)
            
            # Calculate ad metrics
            ad_metrics = self._calculate_ad_metrics(df)
            
            # Calculate delivery metrics
            delivery_metrics = self._calculate_delivery_metrics(df)
            
            # Calculate trends
            trends = self._calculate_trends(df)
            
            # Platform breakdown
            platform_breakdown = self._calculate_platform_breakdown(df, platforms)
            
            return {
                "d2cMetrics": d2c_metrics,
                "adMetrics": ad_metrics,
                "deliveryMetrics": delivery_metrics,
                "trends": trends,
                "platformBreakdown": platform_breakdown,
                "timeSeriesData": raw_data,
                "summary": {
                    "totalRevenue": d2c_metrics.get("totalRevenue", 0),
                    "totalOrders": d2c_metrics.get("totalOrders", 0),
                    "totalCustomers": d2c_metrics.get("newCustomerCount", 0),
                    "roas": ad_metrics.get("returnOnAdSpend", 0),
                    "dataPoints": len(raw_data)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Metrics calculation failed: {e}")
            return self._get_empty_analytics()
    
    def _calculate_d2c_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate D2C business metrics"""
        return {
            "totalRevenue": df["revenue"].sum(),
            "totalOrders": df["orders"].sum(),
            "averageOrderValue": df["avg_order_value"].mean(),
            "newCustomerCount": df["customers"].sum(),
            "grossMerchandiseValue": df["revenue"].sum(),
            "subscriptionRevenue": 0,  # Would need specific data
            "refundAmount": 0,  # Would need specific data
            "costOfGoodsSold": df["revenue"].sum() * 0.4,  # Estimated
            "operatingExpenses": df["revenue"].sum() * 0.2,  # Estimated
            "marketplaceFees": df["revenue"].sum() * 0.03,  # Estimated
            "paymentGatewayFees": df["revenue"].sum() * 0.025,  # Estimated
            "returnProcessingCosts": df["revenue"].sum() * 0.01,  # Estimated
            "overheadCosts": df["revenue"].sum() * 0.15,  # Estimated
            "customerLifetimeValue": df["revenue"].sum() / max(df["customers"].sum(), 1) * 3,  # Estimated
            "customerAcquisitionCost": df["ad_spend"].sum() / max(df["customers"].sum(), 1),
            "repeatPurchaseRate": 25.0,  # Would need specific calculation
            "churnRate": 5.0,  # Would need specific calculation
            "returningCustomerCount": df["customers"].sum() * 0.3,  # Estimated
            "inventoryTurnover": 6.0,  # Would need inventory data
            "stockoutRate": 2.0,  # Would need inventory data
            "daysToSellInventory": 60.0,  # Would need inventory data
        }
    
    def _calculate_ad_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate advertising metrics"""
        total_spend = df["ad_spend"].sum()
        total_revenue = df["conversion_value"].sum()
        total_impressions = df["impressions"].sum()
        total_clicks = df["clicks"].sum()
        total_conversions = df["conversions"].sum()
        
        return {
            "returnOnAdSpend": total_revenue / max(total_spend, 1),
            "clickThroughRate": (total_clicks / max(total_impressions, 1)) * 100,
            "conversionRate": (total_conversions / max(total_clicks, 1)) * 100,
            "costPerClick": total_spend / max(total_clicks, 1),
            "costPerConversion": total_spend / max(total_conversions, 1),
            "impressions": total_impressions,
            "clicks": total_clicks,
            "conversions": total_conversions,
            "adSpend": total_spend,
            "costPerMille": (total_spend / max(total_impressions, 1)) * 1000,
            "costPerAction": total_spend / max(total_conversions, 1),
            "advertisingCostOfSales": (total_spend / max(total_revenue, 1)) * 100
        }
    
    def _calculate_delivery_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate delivery and shipping metrics"""
        return {
            "averageDeliveryTime": df["avg_delivery_hours"].mean() / 24,  # Convert to days
            "shippingCosts": df["shipping_costs"].sum(),
            "onTimeDeliveryRate": 85.0,  # Would need specific calculation
            "lateDeliveryRate": 15.0,  # Would need specific calculation
            "failedDeliveryAttempts": 0,  # Would need specific data
            "returnRate": 8.0,  # Would need specific calculation
            "returnProcessingTime": 3.0,  # Would need specific data
            "pickupSuccessRate": 95.0,  # Would need specific calculation
            "totalShipments": df["shipments"].sum(),
            "averageShippingCost": df["shipping_costs"].sum() / max(df["shipments"].sum(), 1)
        }
    
    def _calculate_trends(self, df: pd.DataFrame) -> Dict[str, List[Dict]]:
        """Calculate trend data"""
        df_sorted = df.sort_values("date")
        
        return {
            "revenue": [
                {"date": row["date"], "value": row["revenue"]} 
                for _, row in df_sorted.iterrows()
            ],
            "orders": [
                {"date": row["date"], "value": row["orders"]} 
                for _, row in df_sorted.iterrows()
            ],
            "customers": [
                {"date": row["date"], "value": row["customers"]} 
                for _, row in df_sorted.iterrows()
            ],
            "roas": [
                {"date": row["date"], "value": row["roas"]} 
                for _, row in df_sorted.iterrows()
            ]
        }
    
    def _calculate_platform_breakdown(self, df: pd.DataFrame, platforms: List[str]) -> Dict[str, Dict[str, float]]:
        """Calculate platform-wise breakdown"""
        total_revenue = df["revenue"].sum()
        
        # This is a simplified breakdown - in reality, you'd need platform-specific data
        return {
            "shopify": {
                "revenue": total_revenue * 0.7,
                "orders": df["orders"].sum() * 0.7,
                "customers": df["customers"].sum() * 0.7
            },
            "facebook": {
                "adSpend": df["ad_spend"].sum() * 0.6,
                "conversions": df["conversions"].sum() * 0.6,
                "roas": df["roas"].mean()
            },
            "google": {
                "adSpend": df["ad_spend"].sum() * 0.4,
                "conversions": df["conversions"].sum() * 0.4,
                "roas": df["roas"].mean()
            },
            "shiprocket": {
                "shippingCosts": df["shipping_costs"].sum(),
                "shipments": df["shipments"].sum(),
                "avgDeliveryTime": df["avg_delivery_hours"].mean() / 24
            }
        }
    
    def _get_empty_analytics(self) -> Dict[str, Any]:
        """Return empty analytics structure"""
        return {
            "d2cMetrics": {},
            "adMetrics": {},
            "deliveryMetrics": {},
            "trends": {},
            "platformBreakdown": {},
            "timeSeriesData": [],
            "summary": {
                "totalRevenue": 0,
                "totalOrders": 0,
                "totalCustomers": 0,
                "roas": 0,
                "dataPoints": 0
            }
        }