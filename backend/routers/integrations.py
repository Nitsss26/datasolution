from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import asyncio

from database import get_database
from utils.bigquery_client import BigQueryClient
from integrations.shopify_client import ShopifyClient
from integrations.facebook_client import FacebookClient
from integrations.google_ads_client import GoogleAdsClient
from integrations.shiprocket_client import ShiprocketClient

router = APIRouter()

# Pydantic models
class PlatformCredentials(BaseModel):
    platform_id: str
    credentials: Dict[str, Any]

class BigQueryConfig(BaseModel):
    project_id: str
    dataset_id: str
    credentials_json: str
    location: str = "US"

class GeminiConfig(BaseModel):
    api_key: str
    model: str = "gemini-pro"

class SyncSettings(BaseModel):
    auto_sync: bool = True
    sync_frequency: str = "hourly"
    data_retention_days: int = 365
    enable_real_time: bool = False

class DataSyncRequest(BaseModel):
    platforms: List[str]
    force_refresh: bool = False
    date_range: Optional[Dict[str, str]] = None

@router.get("/config")
async def get_configurations():
    """Get all integration configurations"""
    try:
        db = await get_database()
        
        # Get platform configurations
        platforms = await db.platform_configs.find({}).to_list(length=None)
        
        # Get BigQuery configuration
        bigquery_config = await db.integration_configs.find_one({"type": "bigquery"})
        
        # Get Gemini configuration
        gemini_config = await db.integration_configs.find_one({"type": "gemini"})
        
        # Get sync settings
        sync_settings = await db.integration_configs.find_one({"type": "sync_settings"})
        
        return {
            "platforms": platforms or [],
            "bigquery": bigquery_config.get("config", {}) if bigquery_config else {},
            "gemini": gemini_config.get("config", {}) if gemini_config else {},
            "sync_settings": sync_settings.get("config", {}) if sync_settings else {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get configurations: {str(e)}")

@router.post("/config/{config_type}")
async def save_configuration(config_type: str, config: Dict[str, Any]):
    """Save integration configuration"""
    try:
        db = await get_database()
        
        if config_type == "platforms":
            # Save platform configurations
            for platform in config:
                await db.platform_configs.update_one(
                    {"platform_id": platform["id"]},
                    {"$set": {
                        "platform_id": platform["id"],
                        "name": platform["name"],
                        "credentials": platform["credentials"],
                        "connected": platform.get("connected", False),
                        "status": platform.get("status", "disconnected"),
                        "updated_at": datetime.utcnow()
                    }},
                    upsert=True
                )
        else:
            # Save other configurations
            await db.integration_configs.update_one(
                {"type": config_type},
                {"$set": {
                    "type": config_type,
                    "config": config,
                    "updated_at": datetime.utcnow()
                }},
                upsert=True
            )
        
        return {"message": f"{config_type} configuration saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save configuration: {str(e)}")

@router.post("/{platform_id}/test")
async def test_platform_connection(platform_id: str, credentials: Dict[str, Any]):
    """Test connection to a specific platform"""
    try:
        if platform_id == "shopify":
            client = ShopifyClient(
                shop_domain=credentials.get("shop_domain"),
                access_token=credentials.get("access_token")
            )
            result = await client.test_connection()
            
        elif platform_id == "facebook":
            client = FacebookClient(
                access_token=credentials.get("access_token"),
                ad_account_id=credentials.get("ad_account_id")
            )
            result = await client.test_connection()
            
        elif platform_id == "google":
            client = GoogleAdsClient(
                developer_token=credentials.get("developer_token"),
                client_id=credentials.get("client_id"),
                client_secret=credentials.get("client_secret"),
                refresh_token=credentials.get("refresh_token"),
                customer_id=credentials.get("customer_id")
            )
            result = await client.test_connection()
            
        elif platform_id == "shiprocket":
            client = ShiprocketClient(
                api_key=credentials.get("api_key"),
                email=credentials.get("email"),
                password=credentials.get("password")
            )
            result = await client.test_connection()
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown platform: {platform_id}")
        
        if result.get("success"):
            # Update platform status in database
            db = await get_database()
            await db.platform_configs.update_one(
                {"platform_id": platform_id},
                {"$set": {
                    "connected": True,
                    "status": "connected",
                    "last_test": datetime.utcnow(),
                    "test_result": result
                }}
            )
            
            return {"success": True, "message": f"{platform_id} connection successful", "data": result}
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Connection failed"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")

@router.get("/{platform_id}/data-preview")
async def get_platform_data_preview(platform_id: str, limit: int = 10):
    """Get a preview of data from a specific platform"""
    try:
        db = await get_database()
        platform_config = await db.platform_configs.find_one({"platform_id": platform_id})
        
        if not platform_config or not platform_config.get("connected"):
            raise HTTPException(status_code=400, detail=f"{platform_id} is not connected")
        
        credentials = platform_config["credentials"]
        
        if platform_id == "shopify":
            client = ShopifyClient(
                shop_domain=credentials.get("shop_domain"),
                access_token=credentials.get("access_token")
            )
            data = await client.get_orders(limit=limit)
            
        elif platform_id == "facebook":
            client = FacebookClient(
                access_token=credentials.get("access_token"),
                ad_account_id=credentials.get("ad_account_id")
            )
            data = await client.get_campaigns(limit=limit)
            
        elif platform_id == "google":
            client = GoogleAdsClient(
                developer_token=credentials.get("developer_token"),
                client_id=credentials.get("client_id"),
                client_secret=credentials.get("client_secret"),
                refresh_token=credentials.get("refresh_token"),
                customer_id=credentials.get("customer_id")
            )
            data = await client.get_campaigns(limit=limit)
            
        elif platform_id == "shiprocket":
            client = ShiprocketClient(
                api_key=credentials.get("api_key"),
                email=credentials.get("email"),
                password=credentials.get("password")
            )
            data = await client.get_shipments(limit=limit)
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown platform: {platform_id}")
        
        return {"platform": platform_id, "data": data, "count": len(data)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data preview: {str(e)}")

@router.post("/sync")
async def trigger_data_sync(request: DataSyncRequest):
    """Trigger data synchronization for specified platforms"""
    try:
        db = await get_database()
        
        # Log sync request
        sync_log = {
            "platforms": request.platforms,
            "force_refresh": request.force_refresh,
            "date_range": request.date_range,
            "status": "initiated",
            "timestamp": datetime.utcnow(),
            "user_id": "default"
        }
        
        await db.sync_logs.insert_one(sync_log)
        
        # Start background sync process
        asyncio.create_task(perform_data_sync(request.platforms, request.force_refresh, request.date_range))
        
        return {
            "message": "Data sync initiated",
            "platforms": request.platforms,
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger sync: {str(e)}")

@router.get("/sync/status")
async def get_sync_status():
    """Get current sync status for all platforms"""
    try:
        db = await get_database()
        
        # Get recent sync logs
        recent_syncs = await db.sync_logs.find({}).sort("timestamp", -1).limit(10).to_list(length=10)
        
        # Get platform statuses
        platforms = await db.platform_configs.find({}).to_list(length=None)
        
        platform_status = []
        for platform in platforms:
            last_sync = await db.sync_logs.find_one(
                {"platforms": {"$in": [platform["platform_id"], "all"]}},
                sort=[("timestamp", -1)]
            )
            
            platform_status.append({
                "platform_id": platform["platform_id"],
                "name": platform["name"],
                "connected": platform.get("connected", False),
                "last_sync": last_sync["timestamp"] if last_sync else None,
                "sync_status": last_sync["status"] if last_sync else "never_synced",
                "data_count": await get_platform_data_count(platform["platform_id"])
            })
        
        return {
            "platforms": platform_status,
            "recent_syncs": recent_syncs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sync status: {str(e)}")

@router.post("/bigquery/test")
async def test_bigquery_connection(config: BigQueryConfig):
    """Test BigQuery connection"""
    try:
        # Save credentials temporarily
        credentials_path = "/tmp/bigquery_credentials.json"
        with open(credentials_path, "w") as f:
            f.write(config.credentials_json)
        
        # Test connection
        bigquery_client = BigQueryClient(
            project_id=config.project_id,
            credentials_path=credentials_path
        )
        
        result = await bigquery_client.test_connection()
        
        # Clean up temporary file
        os.remove(credentials_path)
        
        if result.get("success"):
            return {"success": True, "message": "BigQuery connection successful"}
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Connection failed"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery test failed: {str(e)}")

@router.get("/data-tables")
async def get_data_tables():
    """Get available data tables and their schemas"""
    try:
        bigquery_client = BigQueryClient()
        tables = await bigquery_client.list_tables()
        
        table_info = []
        for table in tables:
            schema = await bigquery_client.get_table_schema(table)
            row_count = await bigquery_client.get_table_row_count(table)
            
            table_info.append({
                "table_name": table,
                "schema": schema,
                "row_count": row_count,
                "last_updated": await bigquery_client.get_table_last_modified(table)
            })
        
        return {"tables": table_info}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data tables: {str(e)}")

@router.post("/query")
async def execute_custom_query(query: Dict[str, Any]):
    """Execute custom BigQuery SQL query"""
    try:
        sql_query = query.get("sql")
        if not sql_query:
            raise HTTPException(status_code=400, detail="SQL query is required")
        
        bigquery_client = BigQueryClient()
        result = await bigquery_client.execute_query(sql_query)
        
        return {
            "query": sql_query,
            "results": result,
            "row_count": len(result) if result else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

# Helper functions
async def perform_data_sync(platforms: List[str], force_refresh: bool, date_range: Optional[Dict[str, str]]):
    """Perform actual data synchronization"""
    try:
        db = await get_database()
        
        for platform_id in platforms:
            if platform_id == "all":
                # Sync all connected platforms
                all_platforms = await db.platform_configs.find({"connected": True}).to_list(length=None)
                for platform in all_platforms:
                    await sync_platform_data(platform["platform_id"], force_refresh, date_range)
            else:
                await sync_platform_data(platform_id, force_refresh, date_range)
        
        # Update sync log
        await db.sync_logs.update_one(
            {"platforms": platforms, "status": "initiated"},
            {"$set": {"status": "completed", "completed_at": datetime.utcnow()}},
            sort=[("timestamp", -1)]
        )
        
    except Exception as e:
        # Update sync log with error
        await db.sync_logs.update_one(
            {"platforms": platforms, "status": "initiated"},
            {"$set": {"status": "failed", "error": str(e), "completed_at": datetime.utcnow()}},
            sort=[("timestamp", -1)]
        )

async def sync_platform_data(platform_id: str, force_refresh: bool, date_range: Optional[Dict[str, str]]):
    """Sync data for a specific platform"""
    try:
        db = await get_database()
        platform_config = await db.platform_configs.find_one({"platform_id": platform_id})
        
        if not platform_config or not platform_config.get("connected"):
            return
        
        credentials = platform_config["credentials"]
        
        if platform_id == "shopify":
            client = ShopifyClient(
                shop_domain=credentials.get("shop_domain"),
                access_token=credentials.get("access_token")
            )
            await client.sync_to_bigquery(force_refresh=force_refresh, date_range=date_range)
            
        elif platform_id == "facebook":
            client = FacebookClient(
                access_token=credentials.get("access_token"),
                ad_account_id=credentials.get("ad_account_id")
            )
            await client.sync_to_bigquery(force_refresh=force_refresh, date_range=date_range)
            
        elif platform_id == "google":
            client = GoogleAdsClient(
                developer_token=credentials.get("developer_token"),
                client_id=credentials.get("client_id"),
                client_secret=credentials.get("client_secret"),
                refresh_token=credentials.get("refresh_token"),
                customer_id=credentials.get("customer_id")
            )
            await client.sync_to_bigquery(force_refresh=force_refresh, date_range=date_range)
            
        elif platform_id == "shiprocket":
            client = ShiprocketClient(
                api_key=credentials.get("api_key"),
                email=credentials.get("email"),
                password=credentials.get("password")
            )
            await client.sync_to_bigquery(force_refresh=force_refresh, date_range=date_range)
        
        # Update last sync time
        await db.platform_configs.update_one(
            {"platform_id": platform_id},
            {"$set": {"last_sync": datetime.utcnow()}}
        )
        
    except Exception as e:
        print(f"Failed to sync {platform_id}: {str(e)}")

async def get_platform_data_count(platform_id: str) -> int:
    """Get data count for a platform from BigQuery"""
    try:
        bigquery_client = BigQueryClient()
        count = await bigquery_client.get_data_count(platform_id)
        return count
    except:
        return 0