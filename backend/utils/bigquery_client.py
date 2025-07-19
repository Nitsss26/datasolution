import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BigQueryClient:
    def __init__(self):
        self.project_id = os.getenv('BIGQUERY_PROJECT_ID', 'd2c-analytics-local')
        self.dataset_id = 'd2c_analytics'
        self.client = None
        self.dataset = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize BigQuery client with credentials"""
        try:
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_path and os.path.exists(credentials_path):
                credentials = service_account.Credentials.from_service_account_file(credentials_path)
                self.client = bigquery.Client(credentials=credentials, project=self.project_id)
            else:
                # For local development without credentials
                os.environ['BIGQUERY_EMULATOR_HOST'] = 'localhost:9050'
                self.client = bigquery.Client(project=self.project_id)
            
            logger.info(f"✅ BigQuery client initialized for project: {self.project_id}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize BigQuery client: {e}")
            self.client = None

    def is_connected(self) -> bool:
        """Check if BigQuery client is connected"""
        try:
            if not self.client:
                return False
            # Test connection by listing datasets
            list(self.client.list_datasets(max_results=1))
            return True
        except Exception as e:
            logger.error(f"BigQuery connection test failed: {e}")
            return False

    async def init_tables(self):
        """Initialize all required BigQuery tables"""
        if not self.client:
            logger.error("BigQuery client not initialized")
            return

        try:
            # Create dataset if it doesn't exist
            dataset_ref = self.client.dataset(self.dataset_id)
            try:
                self.dataset = self.client.get_dataset(dataset_ref)
                logger.info(f"Dataset {self.dataset_id} already exists")
            except Exception:
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = "US"
                self.dataset = self.client.create_dataset(dataset)
                logger.info(f"Created dataset {self.dataset_id}")

            # Define table schemas
            tables_schema = {
                'shopify_orders': [
                    bigquery.SchemaField("order_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("order_number", "STRING"),
                    bigquery.SchemaField("customer_id", "STRING"),
                    bigquery.SchemaField("customer_email", "STRING"),
                    bigquery.SchemaField("total_price", "FLOAT"),
                    bigquery.SchemaField("subtotal_price", "FLOAT"),
                    bigquery.SchemaField("total_tax", "FLOAT"),
                    bigquery.SchemaField("currency", "STRING"),
                    bigquery.SchemaField("financial_status", "STRING"),
                    bigquery.SchemaField("fulfillment_status", "STRING"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                    bigquery.SchemaField("processed_at", "TIMESTAMP"),
                    bigquery.SchemaField("cancelled_at", "TIMESTAMP"),
                    bigquery.SchemaField("tags", "STRING"),
                    bigquery.SchemaField("source_name", "STRING"),
                    bigquery.SchemaField("gateway", "STRING"),
                    bigquery.SchemaField("line_items", "JSON"),
                    bigquery.SchemaField("shipping_address", "JSON"),
                    bigquery.SchemaField("billing_address", "JSON"),
                ],
                'shopify_customers': [
                    bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("email", "STRING"),
                    bigquery.SchemaField("first_name", "STRING"),
                    bigquery.SchemaField("last_name", "STRING"),
                    bigquery.SchemaField("phone", "STRING"),
                    bigquery.SchemaField("orders_count", "INTEGER"),
                    bigquery.SchemaField("total_spent", "FLOAT"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                    bigquery.SchemaField("last_order_date", "TIMESTAMP"),
                    bigquery.SchemaField("tags", "STRING"),
                    bigquery.SchemaField("state", "STRING"),
                    bigquery.SchemaField("country", "STRING"),
                    bigquery.SchemaField("city", "STRING"),
                    bigquery.SchemaField("accepts_marketing", "BOOLEAN"),
                ],
                'shopify_products': [
                    bigquery.SchemaField("product_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("title", "STRING"),
                    bigquery.SchemaField("handle", "STRING"),
                    bigquery.SchemaField("product_type", "STRING"),
                    bigquery.SchemaField("vendor", "STRING"),
                    bigquery.SchemaField("tags", "STRING"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                    bigquery.SchemaField("published_at", "TIMESTAMP"),
                    bigquery.SchemaField("variants", "JSON"),
                    bigquery.SchemaField("images", "JSON"),
                    bigquery.SchemaField("options", "JSON"),
                ],
                'facebook_campaigns': [
                    bigquery.SchemaField("campaign_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("campaign_name", "STRING"),
                    bigquery.SchemaField("account_id", "STRING"),
                    bigquery.SchemaField("objective", "STRING"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("spend", "FLOAT"),
                    bigquery.SchemaField("impressions", "INTEGER"),
                    bigquery.SchemaField("clicks", "INTEGER"),
                    bigquery.SchemaField("conversions", "INTEGER"),
                    bigquery.SchemaField("ctr", "FLOAT"),
                    bigquery.SchemaField("cpc", "FLOAT"),
                    bigquery.SchemaField("cpm", "FLOAT"),
                    bigquery.SchemaField("conversion_rate", "FLOAT"),
                    bigquery.SchemaField("roas", "FLOAT"),
                    bigquery.SchemaField("date_start", "DATE"),
                    bigquery.SchemaField("date_stop", "DATE"),
                    bigquery.SchemaField("created_time", "TIMESTAMP"),
                    bigquery.SchemaField("updated_time", "TIMESTAMP"),
                ],
                'google_campaigns': [
                    bigquery.SchemaField("campaign_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("campaign_name", "STRING"),
                    bigquery.SchemaField("customer_id", "STRING"),
                    bigquery.SchemaField("campaign_type", "STRING"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("cost", "FLOAT"),
                    bigquery.SchemaField("impressions", "INTEGER"),
                    bigquery.SchemaField("clicks", "INTEGER"),
                    bigquery.SchemaField("conversions", "FLOAT"),
                    bigquery.SchemaField("ctr", "FLOAT"),
                    bigquery.SchemaField("avg_cpc", "FLOAT"),
                    bigquery.SchemaField("conversion_rate", "FLOAT"),
                    bigquery.SchemaField("cost_per_conversion", "FLOAT"),
                    bigquery.SchemaField("date", "DATE"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                ],
                'shiprocket_shipments': [
                    bigquery.SchemaField("shipment_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("order_id", "STRING"),
                    bigquery.SchemaField("awb", "STRING"),
                    bigquery.SchemaField("courier_name", "STRING"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("pickup_date", "TIMESTAMP"),
                    bigquery.SchemaField("delivered_date", "TIMESTAMP"),
                    bigquery.SchemaField("expected_delivery_date", "TIMESTAMP"),
                    bigquery.SchemaField("weight", "FLOAT"),
                    bigquery.SchemaField("length", "FLOAT"),
                    bigquery.SchemaField("breadth", "FLOAT"),
                    bigquery.SchemaField("height", "FLOAT"),
                    bigquery.SchemaField("shipping_charges", "FLOAT"),
                    bigquery.SchemaField("cod_charges", "FLOAT"),
                    bigquery.SchemaField("pickup_location", "STRING"),
                    bigquery.SchemaField("delivery_location", "STRING"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                ],
                'analytics_summary': [
                    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
                    bigquery.SchemaField("platform", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("revenue", "FLOAT"),
                    bigquery.SchemaField("orders", "INTEGER"),
                    bigquery.SchemaField("customers", "INTEGER"),
                    bigquery.SchemaField("ad_spend", "FLOAT"),
                    bigquery.SchemaField("impressions", "INTEGER"),
                    bigquery.SchemaField("clicks", "INTEGER"),
                    bigquery.SchemaField("conversions", "INTEGER"),
                    bigquery.SchemaField("roas", "FLOAT"),
                    bigquery.SchemaField("aov", "FLOAT"),
                    bigquery.SchemaField("cac", "FLOAT"),
                    bigquery.SchemaField("ltv", "FLOAT"),
                    bigquery.SchemaField("shipping_cost", "FLOAT"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                ]
            }

            # Create tables
            for table_name, schema in tables_schema.items():
                table_ref = self.dataset.table(table_name)
                try:
                    self.client.get_table(table_ref)
                    logger.info(f"Table {table_name} already exists")
                except Exception:
                    table = bigquery.Table(table_ref, schema=schema)
                    table = self.client.create_table(table)
                    logger.info(f"Created table {table_name}")

            logger.info("✅ All BigQuery tables initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize BigQuery tables: {e}")

    async def insert_data(self, table_name: str, data: List[Dict[str, Any]]):
        """Insert data into BigQuery table"""
        if not self.client or not data:
            return

        try:
            table_ref = self.client.dataset(self.dataset_id).table(table_name)
            table = self.client.get_table(table_ref)
            
            errors = self.client.insert_rows_json(table, data)
            if errors:
                logger.error(f"Failed to insert data into {table_name}: {errors}")
            else:
                logger.info(f"✅ Inserted {len(data)} rows into {table_name}")

        except Exception as e:
            logger.error(f"❌ Failed to insert data into {table_name}: {e}")

    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a BigQuery SQL query"""
        if not self.client:
            return []

        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            rows = []
            for row in results:
                rows.append(dict(row))
            
            return rows

        except Exception as e:
            logger.error(f"❌ Failed to execute query: {e}")
            return []

    async def get_data_count(self, platform: str) -> int:
        """Get data count for a platform"""
        try:
            if platform == "shopify":
                query = f"SELECT COUNT(*) as count FROM `{self.project_id}.{self.dataset_id}.shopify_orders`"
            elif platform == "facebook":
                query = f"SELECT COUNT(*) as count FROM `{self.project_id}.{self.dataset_id}.facebook_campaigns`"
            elif platform == "google":
                query = f"SELECT COUNT(*) as count FROM `{self.project_id}.{self.dataset_id}.google_campaigns`"
            elif platform == "shiprocket":
                query = f"SELECT COUNT(*) as count FROM `{self.project_id}.{self.dataset_id}.shiprocket_shipments`"
            else:
                return 0

            results = await self.execute_query(query)
            return results[0]['count'] if results else 0

        except Exception as e:
            logger.error(f"Failed to get data count for {platform}: {e}")
            return 0

    async def get_analytics_data(self, platforms: List[str], time_range: str = "30d") -> Dict[str, Any]:
        """Get comprehensive analytics data"""
        try:
            # Calculate date range
            days = int(time_range.replace('d', ''))
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            analytics = {
                'revenue': await self._get_revenue_data(platforms, start_date),
                'orders': await self._get_orders_data(platforms, start_date),
                'customers': await self._get_customers_data(platforms, start_date),
                'ad_performance': await self._get_ad_performance(platforms, start_date),
                'delivery_metrics': await self._get_delivery_metrics(start_date),
                'pl_data': await self._get_pl_data(platforms, start_date)
            }
            
            return analytics

        except Exception as e:
            logger.error(f"Failed to get analytics data: {e}")
            return {}

    async def _get_revenue_data(self, platforms: List[str], start_date: str) -> Dict[str, Any]:
        """Get revenue analytics"""
        try:
            query = f"""
            SELECT 
                DATE(created_at) as date,
                SUM(total_price) as revenue,
                COUNT(*) as orders,
                AVG(total_price) as aov
            FROM `{self.project_id}.{self.dataset_id}.shopify_orders`
            WHERE DATE(created_at) >= '{start_date}'
            GROUP BY DATE(created_at)
            ORDER BY date
            """
            
            results = await self.execute_query(query)
            return {
                'daily_revenue': results,
                'total_revenue': sum(row['revenue'] for row in results),
                'total_orders': sum(row['orders'] for row in results),
                'avg_aov': sum(row['aov'] for row in results) / len(results) if results else 0
            }

        except Exception as e:
            logger.error(f"Failed to get revenue data: {e}")
            return {}

    async def _get_orders_data(self, platforms: List[str], start_date: str) -> Dict[str, Any]:
        """Get orders analytics"""
        try:
            query = f"""
            SELECT 
                financial_status,
                fulfillment_status,
                COUNT(*) as count,
                SUM(total_price) as value
            FROM `{self.project_id}.{self.dataset_id}.shopify_orders`
            WHERE DATE(created_at) >= '{start_date}'
            GROUP BY financial_status, fulfillment_status
            """
            
            results = await self.execute_query(query)
            return {'order_status': results}

        except Exception as e:
            logger.error(f"Failed to get orders data: {e}")
            return {}

    async def _get_customers_data(self, platforms: List[str], start_date: str) -> Dict[str, Any]:
        """Get customer analytics"""
        try:
            query = f"""
            SELECT 
                COUNT(*) as total_customers,
                AVG(total_spent) as avg_ltv,
                AVG(orders_count) as avg_orders_per_customer
            FROM `{self.project_id}.{self.dataset_id}.shopify_customers`
            WHERE DATE(created_at) >= '{start_date}'
            """
            
            results = await self.execute_query(query)
            return results[0] if results else {}

        except Exception as e:
            logger.error(f"Failed to get customers data: {e}")
            return {}

    async def _get_ad_performance(self, platforms: List[str], start_date: str) -> Dict[str, Any]:
        """Get advertising performance data"""
        try:
            ad_data = {}
            
            # Facebook Ads
            if 'facebook' in platforms or 'all' in platforms:
                fb_query = f"""
                SELECT 
                    SUM(spend) as total_spend,
                    SUM(impressions) as total_impressions,
                    SUM(clicks) as total_clicks,
                    SUM(conversions) as total_conversions,
                    AVG(roas) as avg_roas
                FROM `{self.project_id}.{self.dataset_id}.facebook_campaigns`
                WHERE date_start >= '{start_date}'
                """
                fb_results = await self.execute_query(fb_query)
                ad_data['facebook'] = fb_results[0] if fb_results else {}

            # Google Ads
            if 'google' in platforms or 'all' in platforms:
                google_query = f"""
                SELECT 
                    SUM(cost) as total_spend,
                    SUM(impressions) as total_impressions,
                    SUM(clicks) as total_clicks,
                    SUM(conversions) as total_conversions,
                    AVG(conversion_rate) as avg_conversion_rate
                FROM `{self.project_id}.{self.dataset_id}.google_campaigns`
                WHERE date >= '{start_date}'
                """
                google_results = await self.execute_query(google_query)
                ad_data['google'] = google_results[0] if google_results else {}

            return ad_data

        except Exception as e:
            logger.error(f"Failed to get ad performance data: {e}")
            return {}

    async def _get_delivery_metrics(self, start_date: str) -> Dict[str, Any]:
        """Get delivery performance metrics"""
        try:
            query = f"""
            SELECT 
                courier_name,
                COUNT(*) as total_shipments,
                AVG(DATETIME_DIFF(delivered_date, pickup_date, DAY)) as avg_delivery_days,
                SUM(shipping_charges) as total_shipping_cost,
                COUNT(CASE WHEN status = 'delivered' THEN 1 END) / COUNT(*) * 100 as delivery_success_rate
            FROM `{self.project_id}.{self.dataset_id}.shiprocket_shipments`
            WHERE DATE(created_at) >= '{start_date}'
            GROUP BY courier_name
            """
            
            results = await self.execute_query(query)
            return {'courier_performance': results}

        except Exception as e:
            logger.error(f"Failed to get delivery metrics: {e}")
            return {}

    async def _get_pl_data(self, platforms: List[str], start_date: str) -> Dict[str, Any]:
        """Get P&L data"""
        try:
            # Revenue
            revenue_query = f"""
            SELECT SUM(total_price) as total_revenue
            FROM `{self.project_id}.{self.dataset_id}.shopify_orders`
            WHERE DATE(created_at) >= '{start_date}'
            """
            revenue_results = await self.execute_query(revenue_query)
            total_revenue = revenue_results[0]['total_revenue'] if revenue_results else 0

            # Ad Spend
            ad_spend_query = f"""
            SELECT 
                (SELECT COALESCE(SUM(spend), 0) FROM `{self.project_id}.{self.dataset_id}.facebook_campaigns` WHERE date_start >= '{start_date}') +
                (SELECT COALESCE(SUM(cost), 0) FROM `{self.project_id}.{self.dataset_id}.google_campaigns` WHERE date >= '{start_date}') as total_ad_spend
            """
            ad_spend_results = await self.execute_query(ad_spend_query)
            total_ad_spend = ad_spend_results[0]['total_ad_spend'] if ad_spend_results else 0

            # Shipping Costs
            shipping_query = f"""
            SELECT SUM(shipping_charges) as total_shipping_cost
            FROM `{self.project_id}.{self.dataset_id}.shiprocket_shipments`
            WHERE DATE(created_at) >= '{start_date}'
            """
            shipping_results = await self.execute_query(shipping_query)
            total_shipping_cost = shipping_results[0]['total_shipping_cost'] if shipping_results else 0

            # Calculate P&L
            cogs = total_revenue * 0.4  # Assume 40% COGS
            platform_fees = total_revenue * 0.05  # Assume 5% platform fees
            other_expenses = total_revenue * 0.08  # Assume 8% other expenses

            total_costs = cogs + total_ad_spend + total_shipping_cost + platform_fees + other_expenses
            gross_profit = total_revenue - cogs
            net_profit = total_revenue - total_costs

            return {
                'revenue': {
                    'total_revenue': total_revenue,
                    'shopify_sales': total_revenue * 0.7,
                    'amazon_sales': total_revenue * 0.2,
                    'other_sales': total_revenue * 0.1
                },
                'costs': {
                    'cogs': cogs,
                    'ad_spend': total_ad_spend,
                    'shipping_cost': total_shipping_cost,
                    'platform_fees': platform_fees,
                    'other_expenses': other_expenses,
                    'total_costs': total_costs
                },
                'profit': {
                    'gross_profit': gross_profit,
                    'net_profit': net_profit,
                    'gross_margin': (gross_profit / total_revenue * 100) if total_revenue > 0 else 0,
                    'net_margin': (net_profit / total_revenue * 100) if total_revenue > 0 else 0
                }
            }

        except Exception as e:
            logger.error(f"Failed to get P&L data: {e}")
            return {}

    async def list_tables(self) -> List[str]:
        """List all tables in the dataset"""
        try:
            if not self.client:
                return []
            
            dataset_ref = self.client.dataset(self.dataset_id)
            tables = self.client.list_tables(dataset_ref)
            return [table.table_id for table in tables]

        except Exception as e:
            logger.error(f"Failed to list tables: {e}")
            return []