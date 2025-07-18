import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BigQueryClient:
    def __init__(self, project_id: str = None, credentials_path: str = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.dataset_id = os.getenv("BIGQUERY_DATASET_ID", "d2c_analytics")
        
        # Initialize credentials
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = bigquery.Client(credentials=credentials, project=self.project_id)
        elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"):
            credentials_info = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
            self.client = bigquery.Client(credentials=credentials, project=self.project_id)
        else:
            # Use default credentials
            self.client = bigquery.Client(project=self.project_id)
    
    async def init_tables(self):
        """Initialize all required BigQuery tables"""
        try:
            # Create dataset if not exists
            await self.create_dataset()
            
            # Define table schemas
            table_schemas = {
                "shopify_orders": [
                    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("order_number", "STRING"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                    bigquery.SchemaField("total_price", "FLOAT"),
                    bigquery.SchemaField("subtotal_price", "FLOAT"),
                    bigquery.SchemaField("total_tax", "FLOAT"),
                    bigquery.SchemaField("currency", "STRING"),
                    bigquery.SchemaField("financial_status", "STRING"),
                    bigquery.SchemaField("fulfillment_status", "STRING"),
                    bigquery.SchemaField("customer_id", "STRING"),
                    bigquery.SchemaField("email", "STRING"),
                    bigquery.SchemaField("phone", "STRING"),
                    bigquery.SchemaField("billing_address", "JSON"),
                    bigquery.SchemaField("shipping_address", "JSON"),
                    bigquery.SchemaField("line_items", "JSON"),
                    bigquery.SchemaField("tags", "STRING"),
                    bigquery.SchemaField("source_name", "STRING"),
                    bigquery.SchemaField("referring_site", "STRING"),
                    bigquery.SchemaField("landing_site", "STRING"),
                    bigquery.SchemaField("platform", "STRING"),
                    bigquery.SchemaField("sync_timestamp", "TIMESTAMP")
                ],
                "shopify_customers": [
                    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("email", "STRING"),
                    bigquery.SchemaField("first_name", "STRING"),
                    bigquery.SchemaField("last_name", "STRING"),
                    bigquery.SchemaField("phone", "STRING"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                    bigquery.SchemaField("orders_count", "INTEGER"),
                    bigquery.SchemaField("total_spent", "FLOAT"),
                    bigquery.SchemaField("state", "STRING"),
                    bigquery.SchemaField("tags", "STRING"),
                    bigquery.SchemaField("accepts_marketing", "BOOLEAN"),
                    bigquery.SchemaField("addresses", "JSON"),
                    bigquery.SchemaField("default_address", "JSON"),
                    bigquery.SchemaField("platform", "STRING"),
                    bigquery.SchemaField("sync_timestamp", "TIMESTAMP")
                ],
                "shopify_products": [
                    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("title", "STRING"),
                    bigquery.SchemaField("handle", "STRING"),
                    bigquery.SchemaField("product_type", "STRING"),
                    bigquery.SchemaField("vendor", "STRING"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP"),
                    bigquery.SchemaField("published_at", "TIMESTAMP"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("tags", "STRING"),
                    bigquery.SchemaField("variants", "JSON"),
                    bigquery.SchemaField("images", "JSON"),
                    bigquery.SchemaField("options", "JSON"),
                    bigquery.SchemaField("platform", "STRING"),
                    bigquery.SchemaField("sync_timestamp", "TIMESTAMP")
                ],
                "facebook_campaigns": [
                    bigquery.SchemaField("campaign_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("campaign_name", "STRING"),
                    bigquery.SchemaField("account_id", "STRING"),
                    bigquery.SchemaField("date_start", "DATE"),
                    bigquery.SchemaField("date_stop", "DATE"),
                    bigquery.SchemaField("impressions", "INTEGER"),
                    bigquery.SchemaField("clicks", "INTEGER"),
                    bigquery.SchemaField("spend", "FLOAT"),
                    bigquery.SchemaField("reach", "INTEGER"),
                    bigquery.SchemaField("frequency", "FLOAT"),
                    bigquery.SchemaField("cpm", "FLOAT"),
                    bigquery.SchemaField("cpc", "FLOAT"),
                    bigquery.SchemaField("ctr", "FLOAT"),
                    bigquery.SchemaField("conversions", "INTEGER"),
                    bigquery.SchemaField("conversion_value", "FLOAT"),
                    bigquery.SchemaField("cost_per_conversion", "FLOAT"),
                    bigquery.SchemaField("roas", "FLOAT"),
                    bigquery.SchemaField("objective", "STRING"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("platform", "STRING"),
                    bigquery.SchemaField("sync_timestamp", "TIMESTAMP")
                ],
                "google_campaigns": [
                    bigquery.SchemaField("campaign_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("campaign_name", "STRING"),
                    bigquery.SchemaField("customer_id", "STRING"),
                    bigquery.SchemaField("date", "DATE"),
                    bigquery.SchemaField("impressions", "INTEGER"),
                    bigquery.SchemaField("clicks", "INTEGER"),
                    bigquery.SchemaField("cost", "INTEGER"),
                    bigquery.SchemaField("conversions", "FLOAT"),
                    bigquery.SchemaField("conversion_value", "FLOAT"),
                    bigquery.SchemaField("ctr", "FLOAT"),
                    bigquery.SchemaField("average_cpc", "INTEGER"),
                    bigquery.SchemaField("cost_per_conversion", "FLOAT"),
                    bigquery.SchemaField("value_per_conversion", "FLOAT"),
                    bigquery.SchemaField("campaign_status", "STRING"),
                    bigquery.SchemaField("campaign_type", "STRING"),
                    bigquery.SchemaField("bidding_strategy", "STRING"),
                    bigquery.SchemaField("platform", "STRING"),
                    bigquery.SchemaField("sync_timestamp", "TIMESTAMP")
                ],
                "shiprocket_shipments": [
                    bigquery.SchemaField("shipment_id", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("order_id", "STRING"),
                    bigquery.SchemaField("awb", "STRING"),
                    bigquery.SchemaField("courier_name", "STRING"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("pickup_date", "DATE"),
                    bigquery.SchemaField("delivered_date", "DATE"),
                    bigquery.SchemaField("expected_delivery_date", "DATE"),
                    bigquery.SchemaField("shipping_charges", "FLOAT"),
                    bigquery.SchemaField("cod_charges", "FLOAT"),
                    bigquery.SchemaField("weight", "FLOAT"),
                    bigquery.SchemaField("length", "FLOAT"),
                    bigquery.SchemaField("breadth", "FLOAT"),
                    bigquery.SchemaField("height", "FLOAT"),
                    bigquery.SchemaField("pickup_address", "JSON"),
                    bigquery.SchemaField("delivery_address", "JSON"),
                    bigquery.SchemaField("tracking_data", "JSON"),
                    bigquery.SchemaField("platform", "STRING"),
                    bigquery.SchemaField("sync_timestamp", "TIMESTAMP")
                ],
                "analytics_summary": [
                    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
                    bigquery.SchemaField("platform", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("total_revenue", "FLOAT"),
                    bigquery.SchemaField("total_orders", "INTEGER"),
                    bigquery.SchemaField("total_customers", "INTEGER"),
                    bigquery.SchemaField("avg_order_value", "FLOAT"),
                    bigquery.SchemaField("ad_spend", "FLOAT"),
                    bigquery.SchemaField("roas", "FLOAT"),
                    bigquery.SchemaField("shipping_cost", "FLOAT"),
                    bigquery.SchemaField("gross_profit", "FLOAT"),
                    bigquery.SchemaField("net_profit", "FLOAT"),
                    bigquery.SchemaField("cac", "FLOAT"),
                    bigquery.SchemaField("ltv", "FLOAT"),
                    bigquery.SchemaField("sync_timestamp", "TIMESTAMP")
                ]
            }
            
            # Create tables
            for table_name, schema in table_schemas.items():
                await self.create_table(table_name, schema)
            
            logger.info("✅ All BigQuery tables initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize BigQuery tables: {e}")
            raise e
    
    async def create_dataset(self):
        """Create BigQuery dataset if it doesn't exist"""
        try:
            dataset_ref = self.client.dataset(self.dataset_id)
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            dataset.description = "D2C Analytics Platform Data Warehouse"
            
            self.client.create_dataset(dataset, exists_ok=True)
            logger.info(f"✅ Dataset {self.dataset_id} created/verified")
            
        except Exception as e:
            logger.error(f"❌ Failed to create dataset: {e}")
            raise e
    
    async def create_table(self, table_name: str, schema: List[bigquery.SchemaField]):
        """Create BigQuery table if it doesn't exist"""
        try:
            table_ref = self.client.dataset(self.dataset_id).table(table_name)
            table = bigquery.Table(table_ref, schema=schema)
            
            # Set table options
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="sync_timestamp"
            )
            
            self.client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table {table_name} created/verified")
            
        except Exception as e:
            logger.error(f"❌ Failed to create table {table_name}: {e}")
            raise e
    
    async def insert_data(self, table_name: str, data: List[Dict[str, Any]]):
        """Insert data into BigQuery table"""
        try:
            if not data:
                return
            
            table_ref = self.client.dataset(self.dataset_id).table(table_name)
            table = self.client.get_table(table_ref)
            
            # Add sync timestamp to all records
            for record in data:
                record['sync_timestamp'] = datetime.utcnow()
            
            errors = self.client.insert_rows_json(table, data)
            
            if errors:
                logger.error(f"❌ Failed to insert data into {table_name}: {errors}")
                raise Exception(f"Insert errors: {errors}")
            
            logger.info(f"✅ Inserted {len(data)} rows into {table_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to insert data into {table_name}: {e}")
            raise e
    
    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute BigQuery SQL query"""
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convert to list of dictionaries
            data = []
            for row in results:
                data.append(dict(row))
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Query execution failed: {e}")
            raise e
    
    async def get_analytics_summary(self, platforms: List[str], date_range: Dict[str, str]) -> Dict[str, Any]:
        """Get comprehensive analytics summary"""
        try:
            platform_filter = ""
            if platforms and "all" not in platforms:
                platform_list = "', '".join(platforms)
                platform_filter = f"AND platform IN ('{platform_list}')"
            
            query = f"""
            SELECT 
                platform,
                DATE(sync_timestamp) as date,
                COUNT(*) as total_records,
                SUM(CASE WHEN platform = 'shopify' THEN CAST(total_price AS FLOAT64) ELSE 0 END) as shopify_revenue,
                SUM(CASE WHEN platform = 'facebook' THEN CAST(spend AS FLOAT64) ELSE 0 END) as facebook_spend,
                SUM(CASE WHEN platform = 'google' THEN CAST(cost AS FLOAT64)/1000000 ELSE 0 END) as google_spend,
                SUM(CASE WHEN platform = 'shiprocket' THEN CAST(shipping_charges AS FLOAT64) ELSE 0 END) as shipping_cost
            FROM (
                SELECT 'shopify' as platform, total_price, NULL as spend, NULL as cost, NULL as shipping_charges, sync_timestamp
                FROM `{self.project_id}.{self.dataset_id}.shopify_orders`
                WHERE DATE(sync_timestamp) BETWEEN '{date_range.get("start_date")}' AND '{date_range.get("end_date")}'
                
                UNION ALL
                
                SELECT 'facebook' as platform, NULL as total_price, spend, NULL as cost, NULL as shipping_charges, sync_timestamp
                FROM `{self.project_id}.{self.dataset_id}.facebook_campaigns`
                WHERE date_start BETWEEN '{date_range.get("start_date")}' AND '{date_range.get("end_date")}'
                
                UNION ALL
                
                SELECT 'google' as platform, NULL as total_price, NULL as spend, cost, NULL as shipping_charges, sync_timestamp
                FROM `{self.project_id}.{self.dataset_id}.google_campaigns`
                WHERE date BETWEEN '{date_range.get("start_date")}' AND '{date_range.get("end_date")}'
                
                UNION ALL
                
                SELECT 'shiprocket' as platform, NULL as total_price, NULL as spend, NULL as cost, shipping_charges, sync_timestamp
                FROM `{self.project_id}.{self.dataset_id}.shiprocket_shipments`
                WHERE DATE(sync_timestamp) BETWEEN '{date_range.get("start_date")}' AND '{date_range.get("end_date")}'
            )
            WHERE 1=1 {platform_filter}
            GROUP BY platform, DATE(sync_timestamp)
            ORDER BY date DESC, platform
            """
            
            return await self.execute_query(query)
            
        except Exception as e:
            logger.error(f"❌ Failed to get analytics summary: {e}")
            raise e
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test BigQuery connection"""
        try:
            # Simple query to test connection
            query = f"SELECT 1 as test_value"
            result = await self.execute_query(query)
            
            if result:
                return {"success": True, "message": "BigQuery connection successful"}
            else:
                return {"success": False, "error": "No results returned"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_tables(self) -> List[str]:
        """List all tables in the dataset"""
        try:
            dataset_ref = self.client.dataset(self.dataset_id)
            tables = self.client.list_tables(dataset_ref)
            return [table.table_id for table in tables]
            
        except Exception as e:
            logger.error(f"❌ Failed to list tables: {e}")
            return []
    
    async def get_table_schema(self, table_name: str) -> List[Dict[str, str]]:
        """Get table schema"""
        try:
            table_ref = self.client.dataset(self.dataset_id).table(table_name)
            table = self.client.get_table(table_ref)
            
            schema = []
            for field in table.schema:
                schema.append({
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description or ""
                })
            
            return schema
            
        except Exception as e:
            logger.error(f"❌ Failed to get table schema: {e}")
            return []
    
    async def get_table_row_count(self, table_name: str) -> int:
        """Get table row count"""
        try:
            query = f"SELECT COUNT(*) as count FROM `{self.project_id}.{self.dataset_id}.{table_name}`"
            result = await self.execute_query(query)
            return result[0]["count"] if result else 0
            
        except Exception as e:
            logger.error(f"❌ Failed to get row count: {e}")
            return 0
    
    async def get_table_last_modified(self, table_name: str) -> str:
        """Get table last modified timestamp"""
        try:
            table_ref = self.client.dataset(self.dataset_id).table(table_name)
            table = self.client.get_table(table_ref)
            return table.modified.isoformat() if table.modified else ""
            
        except Exception as e:
            logger.error(f"❌ Failed to get last modified: {e}")
            return ""
    
    def is_connected(self) -> bool:
        """Check if BigQuery client is connected"""
        try:
            # Simple test query
            query = "SELECT 1"
            query_job = self.client.query(query)
            query_job.result()
            return True
        except:
            return False
    
    async def get_data_count(self, platform: str) -> int:
        """Get data count for a specific platform"""
        try:
            table_mapping = {
                "shopify": "shopify_orders",
                "facebook": "facebook_campaigns", 
                "google": "google_campaigns",
                "shiprocket": "shiprocket_shipments"
            }
            
            table_name = table_mapping.get(platform)
            if not table_name:
                return 0
            
            return await self.get_table_row_count(table_name)
            
        except Exception as e:
            logger.error(f"❌ Failed to get data count for {platform}: {e}")
            return 0