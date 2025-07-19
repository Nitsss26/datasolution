import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .bigquery_client import BigQueryClient
from database import get_database

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, bigquery_client: BigQueryClient):
        self.bigquery = bigquery_client
        
    async def sync_all_platforms(self, platforms: List[str], force_refresh: bool = False):
        """Sync data from all specified platforms"""
        try:
            db = await get_database()
            
            # Log sync start
            sync_log = {
                "type": "multi_platform_sync",
                "platforms": platforms,
                "status": "started",
                "timestamp": datetime.utcnow(),
                "force_refresh": force_refresh
            }
            result = await db.sync_logs.insert_one(sync_log)
            sync_id = result.inserted_id
            
            success_count = 0
            error_count = 0
            
            for platform in platforms:
                try:
                    await self.sync_platform_data(platform, force_refresh)
                    success_count += 1
                    logger.info(f"✅ Successfully synced {platform}")
                except Exception as e:
                    error_count += 1
                    logger.error(f"❌ Failed to sync {platform}: {e}")
                    
                    # Log individual platform error
                    await db.error_logs.insert_one({
                        "sync_id": sync_id,
                        "platform": platform,
                        "error": str(e),
                        "timestamp": datetime.utcnow()
                    })
                
                # Rate limiting between platforms
                await asyncio.sleep(1)
            
            # Update sync log
            await db.sync_logs.update_one(
                {"_id": sync_id},
                {"$set": {
                    "status": "completed" if error_count == 0 else "partial",
                    "completed_at": datetime.utcnow(),
                    "success_count": success_count,
                    "error_count": error_count
                }}
            )
            
            logger.info(f"✅ Multi-platform sync completed: {success_count} success, {error_count} errors")
            
        except Exception as e:
            logger.error(f"❌ Multi-platform sync failed: {e}")
            raise

    async def sync_platform_data(self, platform: str, force_refresh: bool = False):
        """Sync data for a specific platform"""
        try:
            db = await get_database()
            
            # Check if platform is configured
            platform_config = await db.platform_configs.find_one({"platform_id": platform})
            if not platform_config:
                # Create demo data for platforms that aren't configured
                await self._create_demo_data(platform)
                return
            
            # Get last sync time
            last_sync = platform_config.get("last_sync")
            if not force_refresh and last_sync:
                # Check if we need to sync (don't sync more than once per hour)
                if datetime.utcnow() - last_sync < timedelta(hours=1):
                    logger.info(f"Skipping {platform} sync - last synced {last_sync}")
                    return
            
            # Perform platform-specific sync
            if platform == "shopify":
                await self._sync_shopify_data(platform_config)
            elif platform == "facebook":
                await self._sync_facebook_data(platform_config)
            elif platform == "google":
                await self._sync_google_data(platform_config)
            elif platform == "shiprocket":
                await self._sync_shiprocket_data(platform_config)
            else:
                logger.warning(f"Unknown platform: {platform}")
                return
            
            # Update last sync time
            await db.platform_configs.update_one(
                {"platform_id": platform},
                {"$set": {"last_sync": datetime.utcnow()}}
            )
            
            logger.info(f"✅ {platform} data sync completed")
            
        except Exception as e:
            logger.error(f"❌ {platform} data sync failed: {e}")
            raise

    async def _create_demo_data(self, platform: str):
        """Create demo data for platforms that aren't configured"""
        try:
            current_date = datetime.utcnow()
            
            if platform == "shopify":
                # Generate demo Shopify orders
                demo_orders = []
                for i in range(100):
                    order_date = current_date - timedelta(days=i % 30)
                    demo_orders.append({
                        "order_id": f"demo_order_{i}",
                        "order_number": f"#{1000 + i}",
                        "customer_id": f"demo_customer_{i % 20}",
                        "customer_email": f"customer{i % 20}@example.com",
                        "total_price": round(50 + (i % 500), 2),
                        "subtotal_price": round(45 + (i % 450), 2),
                        "total_tax": round(5 + (i % 50), 2),
                        "currency": "INR",
                        "financial_status": "paid" if i % 10 != 0 else "pending",
                        "fulfillment_status": "fulfilled" if i % 8 != 0 else "pending",
                        "created_at": order_date,
                        "updated_at": order_date,
                        "processed_at": order_date,
                        "cancelled_at": None,
                        "tags": "demo,online",
                        "source_name": "web",
                        "gateway": "razorpay",
                        "line_items": [{"product_id": f"prod_{i % 10}", "quantity": 1 + (i % 3)}],
                        "shipping_address": {"city": "Mumbai", "country": "India"},
                        "billing_address": {"city": "Mumbai", "country": "India"}
                    })
                
                await self.bigquery.insert_data("shopify_orders", demo_orders)
                
                # Generate demo customers
                demo_customers = []
                for i in range(20):
                    customer_date = current_date - timedelta(days=i * 5)
                    demo_customers.append({
                        "customer_id": f"demo_customer_{i}",
                        "email": f"customer{i}@example.com",
                        "first_name": f"Customer",
                        "last_name": f"{i}",
                        "phone": f"+91{9000000000 + i}",
                        "orders_count": 1 + (i % 10),
                        "total_spent": round(100 + (i * 50), 2),
                        "created_at": customer_date,
                        "updated_at": customer_date,
                        "last_order_date": current_date - timedelta(days=i % 15),
                        "tags": "demo,vip" if i % 5 == 0 else "demo",
                        "state": "Maharashtra",
                        "country": "India",
                        "city": "Mumbai",
                        "accepts_marketing": i % 3 == 0
                    })
                
                await self.bigquery.insert_data("shopify_customers", demo_customers)
                
            elif platform == "facebook":
                # Generate demo Facebook campaigns
                demo_campaigns = []
                for i in range(10):
                    campaign_date = current_date - timedelta(days=i)
                    demo_campaigns.append({
                        "campaign_id": f"demo_fb_campaign_{i}",
                        "campaign_name": f"Demo Campaign {i}",
                        "account_id": "demo_account",
                        "objective": "CONVERSIONS",
                        "status": "ACTIVE",
                        "spend": round(1000 + (i * 200), 2),
                        "impressions": 10000 + (i * 2000),
                        "clicks": 500 + (i * 100),
                        "conversions": 25 + (i * 5),
                        "ctr": round(2.5 + (i * 0.1), 2),
                        "cpc": round(12 + (i * 2), 2),
                        "cpm": round(120 + (i * 10), 2),
                        "conversion_rate": round(5 + (i * 0.5), 2),
                        "roas": round(3.5 + (i * 0.2), 2),
                        "date_start": campaign_date.date(),
                        "date_stop": campaign_date.date(),
                        "created_time": campaign_date,
                        "updated_time": campaign_date
                    })
                
                await self.bigquery.insert_data("facebook_campaigns", demo_campaigns)
                
            elif platform == "google":
                # Generate demo Google campaigns
                demo_campaigns = []
                for i in range(8):
                    campaign_date = current_date - timedelta(days=i)
                    demo_campaigns.append({
                        "campaign_id": f"demo_google_campaign_{i}",
                        "campaign_name": f"Demo Google Campaign {i}",
                        "customer_id": "demo_customer",
                        "campaign_type": "SEARCH",
                        "status": "ENABLED",
                        "cost": round(800 + (i * 150), 2),
                        "impressions": 8000 + (i * 1500),
                        "clicks": 400 + (i * 80),
                        "conversions": round(20 + (i * 3), 1),
                        "ctr": round(3.0 + (i * 0.2), 2),
                        "avg_cpc": round(15 + (i * 1.5), 2),
                        "conversion_rate": round(4.5 + (i * 0.3), 2),
                        "cost_per_conversion": round(35 + (i * 5), 2),
                        "date": campaign_date.date(),
                        "created_at": campaign_date,
                        "updated_at": campaign_date
                    })
                
                await self.bigquery.insert_data("google_campaigns", demo_campaigns)
                
            elif platform == "shiprocket":
                # Generate demo shipments
                demo_shipments = []
                couriers = ["Shiprocket", "Delhivery", "BlueDart", "DTDC"]
                statuses = ["delivered", "in_transit", "picked_up", "delivered"]
                
                for i in range(80):
                    pickup_date = current_date - timedelta(days=i % 20)
                    delivered_date = pickup_date + timedelta(days=2 + (i % 3)) if i % 10 != 0 else None
                    
                    demo_shipments.append({
                        "shipment_id": f"demo_shipment_{i}",
                        "order_id": f"demo_order_{i % 50}",
                        "awb": f"AWB{1000000 + i}",
                        "courier_name": couriers[i % len(couriers)],
                        "status": statuses[i % len(statuses)],
                        "pickup_date": pickup_date,
                        "delivered_date": delivered_date,
                        "expected_delivery_date": pickup_date + timedelta(days=3),
                        "weight": round(0.5 + (i % 5), 2),
                        "length": 10 + (i % 20),
                        "breadth": 8 + (i % 15),
                        "height": 5 + (i % 10),
                        "shipping_charges": round(50 + (i % 100), 2),
                        "cod_charges": round(20 + (i % 30), 2) if i % 3 == 0 else 0,
                        "pickup_location": "Mumbai",
                        "delivery_location": f"City_{i % 10}",
                        "created_at": pickup_date,
                        "updated_at": pickup_date
                    })
                
                await self.bigquery.insert_data("shiprocket_shipments", demo_shipments)
            
            logger.info(f"✅ Created demo data for {platform}")
            
        except Exception as e:
            logger.error(f"❌ Failed to create demo data for {platform}: {e}")

    async def _sync_shopify_data(self, config: Dict[str, Any]):
        """Sync Shopify data using API"""
        # This would use the actual Shopify API
        # For now, we'll create some demo data
        await self._create_demo_data("shopify")

    async def _sync_facebook_data(self, config: Dict[str, Any]):
        """Sync Facebook Ads data using API"""
        # This would use the actual Facebook Ads API
        # For now, we'll create some demo data
        await self._create_demo_data("facebook")

    async def _sync_google_data(self, config: Dict[str, Any]):
        """Sync Google Ads data using API"""
        # This would use the actual Google Ads API
        # For now, we'll create some demo data
        await self._create_demo_data("google")

    async def _sync_shiprocket_data(self, config: Dict[str, Any]):
        """Sync Shiprocket data using API"""
        # This would use the actual Shiprocket API
        # For now, we'll create some demo data
        await self._create_demo_data("shiprocket")

    async def get_analytics(self, platforms: List[str], time_range: str, metrics: Optional[List[str]] = None, granularity: str = "daily") -> Dict[str, Any]:
        """Get comprehensive analytics data"""
        try:
            # Get data from BigQuery
            analytics_data = await self.bigquery.get_analytics_data(platforms, time_range)
            
            # Add calculated metrics
            analytics_data['calculated_metrics'] = await self._calculate_metrics(analytics_data)
            
            # Add summary
            analytics_data['summary'] = await self._generate_summary(analytics_data)
            
            return analytics_data
            
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {}

    async def _calculate_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate additional metrics from raw data"""
        try:
            metrics = {}
            
            # Revenue metrics
            if 'revenue' in data:
                revenue_data = data['revenue']
                metrics['revenue_growth'] = self._calculate_growth_rate(revenue_data.get('daily_revenue', []))
                metrics['revenue_trend'] = self._calculate_trend(revenue_data.get('daily_revenue', []))
            
            # Customer metrics
            if 'customers' in data:
                customer_data = data['customers']
                metrics['customer_acquisition_cost'] = self._calculate_cac(data)
                metrics['customer_lifetime_value'] = customer_data.get('avg_ltv', 0)
            
            # Ad metrics
            if 'ad_performance' in data:
                ad_data = data['ad_performance']
                metrics['total_roas'] = self._calculate_total_roas(ad_data)
                metrics['ad_efficiency'] = self._calculate_ad_efficiency(ad_data)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate metrics: {e}")
            return {}

    def _calculate_growth_rate(self, daily_data: List[Dict[str, Any]]) -> float:
        """Calculate growth rate from daily data"""
        if len(daily_data) < 2:
            return 0.0
        
        # Compare first half vs second half
        mid_point = len(daily_data) // 2
        first_half = sum(day.get('revenue', 0) for day in daily_data[:mid_point])
        second_half = sum(day.get('revenue', 0) for day in daily_data[mid_point:])
        
        if first_half == 0:
            return 0.0
        
        return ((second_half - first_half) / first_half) * 100

    def _calculate_trend(self, daily_data: List[Dict[str, Any]]) -> str:
        """Calculate trend direction"""
        if len(daily_data) < 3:
            return "stable"
        
        recent_avg = sum(day.get('revenue', 0) for day in daily_data[-7:]) / min(7, len(daily_data))
        older_avg = sum(day.get('revenue', 0) for day in daily_data[:-7]) / max(1, len(daily_data) - 7)
        
        if recent_avg > older_avg * 1.1:
            return "increasing"
        elif recent_avg < older_avg * 0.9:
            return "decreasing"
        else:
            return "stable"

    def _calculate_cac(self, data: Dict[str, Any]) -> float:
        """Calculate Customer Acquisition Cost"""
        try:
            ad_data = data.get('ad_performance', {})
            total_ad_spend = 0
            total_conversions = 0
            
            for platform, metrics in ad_data.items():
                total_ad_spend += metrics.get('total_spend', 0)
                total_conversions += metrics.get('total_conversions', 0)
            
            if total_conversions == 0:
                return 0.0
            
            return total_ad_spend / total_conversions
            
        except Exception as e:
            logger.error(f"Failed to calculate CAC: {e}")
            return 0.0

    def _calculate_total_roas(self, ad_data: Dict[str, Any]) -> float:
        """Calculate overall ROAS across all platforms"""
        try:
            total_spend = 0
            total_revenue = 0
            
            for platform, metrics in ad_data.items():
                spend = metrics.get('total_spend', 0)
                conversions = metrics.get('total_conversions', 0)
                total_spend += spend
                # Assume average order value of 1500 INR
                total_revenue += conversions * 1500
            
            if total_spend == 0:
                return 0.0
            
            return total_revenue / total_spend
            
        except Exception as e:
            logger.error(f"Failed to calculate total ROAS: {e}")
            return 0.0

    def _calculate_ad_efficiency(self, ad_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate ad efficiency metrics"""
        try:
            efficiency = {}
            
            for platform, metrics in ad_data.items():
                impressions = metrics.get('total_impressions', 0)
                clicks = metrics.get('total_clicks', 0)
                conversions = metrics.get('total_conversions', 0)
                
                if impressions > 0:
                    ctr = (clicks / impressions) * 100
                    efficiency[f'{platform}_ctr'] = ctr
                
                if clicks > 0:
                    conversion_rate = (conversions / clicks) * 100
                    efficiency[f'{platform}_conversion_rate'] = conversion_rate
            
            return efficiency
            
        except Exception as e:
            logger.error(f"Failed to calculate ad efficiency: {e}")
            return {}

    async def _generate_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary"""
        try:
            summary = {
                'total_revenue': data.get('revenue', {}).get('total_revenue', 0),
                'total_orders': data.get('revenue', {}).get('total_orders', 0),
                'total_customers': data.get('customers', {}).get('total_customers', 0),
                'total_ad_spend': 0,
                'overall_roas': 0,
                'profit_margin': 0
            }
            
            # Calculate total ad spend
            ad_data = data.get('ad_performance', {})
            for platform, metrics in ad_data.items():
                summary['total_ad_spend'] += metrics.get('total_spend', 0)
            
            # Calculate overall ROAS
            if summary['total_ad_spend'] > 0:
                summary['overall_roas'] = summary['total_revenue'] / summary['total_ad_spend']
            
            # Calculate profit margin from P&L data
            pl_data = data.get('pl_data', {})
            profit_info = pl_data.get('profit', {})
            summary['profit_margin'] = profit_info.get('net_margin', 0)
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return {}