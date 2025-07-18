from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
import logging
from utils.bigquery_client import BigQueryClient
from database import get_database

logger = logging.getLogger(__name__)
router = APIRouter()

class PipelineSettings(BaseModel):
    auto_sync: bool = True
    sync_frequency: str = "hourly"
    data_retention_days: int = 365
    enable_real_time: bool = False
    batch_size: int = 1000
    error_retry_count: int = 3
    notification_email: str = ""
    webhook_url: str = ""

class PipelineStatus(BaseModel):
    status: str
    last_run: Optional[str]
    next_run: Optional[str]
    total_records: int
    errors: List[Dict[str, Any]]

@router.get("/status")
async def get_pipeline_status():
    """Get current pipeline status"""
    try:
        db = await get_database()
        bigquery_client = BigQueryClient()
        
        # Get last sync logs
        recent_syncs = await db.sync_logs.find({}).sort("timestamp", -1).limit(5).to_list(length=5)
        
        # Get data counts from BigQuery
        data_counts = {}
        platforms = ["shopify", "facebook", "google", "shiprocket"]
        
        for platform in platforms:
            try:
                count = await bigquery_client.get_data_count(platform)
                data_counts[platform] = count
            except:
                data_counts[platform] = 0
        
        # Get pipeline settings
        pipeline_config = await db.integration_configs.find_one({"type": "pipeline_settings"})
        settings = pipeline_config.get("config", {}) if pipeline_config else {}
        
        return {
            "status": "running" if settings.get("auto_sync", True) else "stopped",
            "last_sync": recent_syncs[0]["timestamp"] if recent_syncs else None,
            "data_counts": data_counts,
            "total_records": sum(data_counts.values()),
            "recent_syncs": recent_syncs,
            "settings": settings
        }
        
    except Exception as e:
        logger.error(f"Failed to get pipeline status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start")
async def start_pipeline(background_tasks: BackgroundTasks):
    """Start the data pipeline"""
    try:
        db = await get_database()
        
        # Update pipeline settings
        await db.integration_configs.update_one(
            {"type": "pipeline_settings"},
            {"$set": {
                "type": "pipeline_settings",
                "config.auto_sync": True,
                "config.status": "running",
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        
        # Start background sync task
        background_tasks.add_task(run_pipeline_sync)
        
        return {"message": "Pipeline started successfully", "status": "running"}
        
    except Exception as e:
        logger.error(f"Failed to start pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_pipeline():
    """Stop the data pipeline"""
    try:
        db = await get_database()
        
        # Update pipeline settings
        await db.integration_configs.update_one(
            {"type": "pipeline_settings"},
            {"$set": {
                "type": "pipeline_settings",
                "config.auto_sync": False,
                "config.status": "stopped",
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        
        return {"message": "Pipeline stopped successfully", "status": "stopped"}
        
    except Exception as e:
        logger.error(f"Failed to stop pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-data")
async def clear_all_data():
    """Clear all data from BigQuery tables"""
    try:
        bigquery_client = BigQueryClient()
        
        # List of tables to clear
        tables = [
            "shopify_orders",
            "shopify_customers", 
            "shopify_products",
            "facebook_campaigns",
            "google_campaigns",
            "shiprocket_shipments",
            "analytics_summary"
        ]
        
        cleared_tables = []
        for table in tables:
            try:
                # Delete all rows from table
                query = f"DELETE FROM `{bigquery_client.project_id}.{bigquery_client.dataset_id}.{table}` WHERE TRUE"
                await bigquery_client.execute_query(query)
                cleared_tables.append(table)
            except Exception as e:
                logger.warning(f"Failed to clear table {table}: {e}")
        
        return {
            "message": "Data cleared successfully",
            "cleared_tables": cleared_tables
        }
        
    except Exception as e:
        logger.error(f"Failed to clear data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-tables")
async def reset_bigquery_tables():
    """Reset BigQuery tables (drop and recreate)"""
    try:
        bigquery_client = BigQueryClient()
        
        # Drop existing tables
        tables = await bigquery_client.list_tables()
        dropped_tables = []
        
        for table in tables:
            try:
                table_ref = bigquery_client.client.dataset(bigquery_client.dataset_id).table(table)
                bigquery_client.client.delete_table(table_ref)
                dropped_tables.append(table)
            except Exception as e:
                logger.warning(f"Failed to drop table {table}: {e}")
        
        # Recreate tables
        await bigquery_client.init_tables()
        
        return {
            "message": "BigQuery tables reset successfully",
            "dropped_tables": dropped_tables,
            "recreated": True
        }
        
    except Exception as e:
        logger.error(f"Failed to reset tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync-platform/{platform_id}")
async def sync_specific_platform(platform_id: str, background_tasks: BackgroundTasks):
    """Sync data for a specific platform"""
    try:
        if platform_id not in ["shopify", "facebook", "google", "shiprocket"]:
            raise HTTPException(status_code=400, detail="Invalid platform ID")
        
        # Start background sync for specific platform
        background_tasks.add_task(sync_platform_data, platform_id)
        
        return {
            "message": f"{platform_id.title()} sync initiated",
            "platform": platform_id,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Failed to sync {platform_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_pipeline_logs(limit: int = 50):
    """Get pipeline execution logs"""
    try:
        db = await get_database()
        
        # Get sync logs
        logs = await db.sync_logs.find({}).sort("timestamp", -1).limit(limit).to_list(length=limit)
        
        # Get error logs
        error_logs = await db.error_logs.find({}).sort("timestamp", -1).limit(20).to_list(length=20)
        
        return {
            "sync_logs": logs,
            "error_logs": error_logs,
            "total_logs": len(logs) + len(error_logs)
        }
        
    except Exception as e:
        logger.error(f"Failed to get pipeline logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings")
async def update_pipeline_settings(settings: PipelineSettings):
    """Update pipeline settings"""
    try:
        db = await get_database()
        
        # Save pipeline settings
        await db.integration_configs.update_one(
            {"type": "pipeline_settings"},
            {"$set": {
                "type": "pipeline_settings",
                "config": settings.dict(),
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        
        return {
            "message": "Pipeline settings updated successfully",
            "settings": settings.dict()
        }
        
    except Exception as e:
        logger.error(f"Failed to update pipeline settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_pipeline_metrics():
    """Get pipeline performance metrics"""
    try:
        db = await get_database()
        bigquery_client = BigQueryClient()
        
        # Get sync statistics
        sync_stats = await db.sync_logs.aggregate([
            {
                "$group": {
                    "_id": "$platform",
                    "total_syncs": {"$sum": 1},
                    "successful_syncs": {
                        "$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}
                    },
                    "failed_syncs": {
                        "$sum": {"$cond": [{"$eq": ["$status", "failed"]}, 1, 0]}
                    },
                    "avg_duration": {"$avg": "$duration"},
                    "last_sync": {"$max": "$timestamp"}
                }
            }
        ]).to_list(length=None)
        
        # Get data volume metrics
        data_volumes = {}
        platforms = ["shopify", "facebook", "google", "shiprocket"]
        
        for platform in platforms:
            try:
                count = await bigquery_client.get_data_count(platform)
                data_volumes[platform] = count
            except:
                data_volumes[platform] = 0
        
        return {
            "sync_statistics": sync_stats,
            "data_volumes": data_volumes,
            "total_records": sum(data_volumes.values()),
            "platforms_connected": len([p for p in platforms if data_volumes[p] > 0])
        }
        
    except Exception as e:
        logger.error(f"Failed to get pipeline metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task functions
async def run_pipeline_sync():
    """Run full pipeline sync"""
    try:
        db = await get_database()
        
        # Log sync start
        sync_log = {
            "type": "full_pipeline_sync",
            "status": "started",
            "timestamp": datetime.utcnow(),
            "platforms": ["shopify", "facebook", "google", "shiprocket"]
        }
        await db.sync_logs.insert_one(sync_log)
        
        # Sync all platforms
        platforms = ["shopify", "facebook", "google", "shiprocket"]
        for platform in platforms:
            await sync_platform_data(platform)
            await asyncio.sleep(2)  # Rate limiting
        
        # Update sync log
        await db.sync_logs.update_one(
            {"_id": sync_log["_id"]},
            {"$set": {
                "status": "completed",
                "completed_at": datetime.utcnow()
            }}
        )
        
        logger.info("✅ Full pipeline sync completed")
        
    except Exception as e:
        logger.error(f"❌ Pipeline sync failed: {e}")
        # Log error
        await db.error_logs.insert_one({
            "type": "pipeline_sync_error",
            "error": str(e),
            "timestamp": datetime.utcnow()
        })

async def sync_platform_data(platform_id: str):
    """Sync data for a specific platform"""
    try:
        db = await get_database()
        
        # Get platform configuration
        platform_config = await db.platform_configs.find_one({"platform_id": platform_id})
        
        if not platform_config or not platform_config.get("connected"):
            logger.warning(f"Platform {platform_id} not connected, skipping sync")
            return
        
        # Import and use appropriate client
        if platform_id == "shopify":
            from integrations.shopify_client import ShopifyClient
            client = ShopifyClient(
                shop_domain=platform_config["credentials"]["shop_domain"],
                access_token=platform_config["credentials"]["access_token"]
            )
        elif platform_id == "facebook":
            from integrations.facebook_client import FacebookClient
            client = FacebookClient(
                access_token=platform_config["credentials"]["access_token"],
                ad_account_id=platform_config["credentials"]["ad_account_id"]
            )
        elif platform_id == "google":
            from integrations.google_ads_client import GoogleAdsClient
            client = GoogleAdsClient(
                developer_token=platform_config["credentials"]["developer_token"],
                client_id=platform_config["credentials"]["client_id"],
                client_secret=platform_config["credentials"]["client_secret"],
                refresh_token=platform_config["credentials"]["refresh_token"],
                customer_id=platform_config["credentials"]["customer_id"]
            )
        elif platform_id == "shiprocket":
            from integrations.shiprocket_client import ShiprocketClient
            client = ShiprocketClient(
                api_key=platform_config["credentials"]["api_key"],
                email=platform_config["credentials"]["email"],
                password=platform_config["credentials"]["password"]
            )
        else:
            logger.error(f"Unknown platform: {platform_id}")
            return
        
        # Perform sync
        await client.sync_to_bigquery()
        
        # Update last sync time
        await db.platform_configs.update_one(
            {"platform_id": platform_id},
            {"$set": {"last_sync": datetime.utcnow()}}
        )
        
        logger.info(f"✅ {platform_id} sync completed")
        
    except Exception as e:
        logger.error(f"❌ {platform_id} sync failed: {e}")
        # Log error
        await db.error_logs.insert_one({
            "type": f"{platform_id}_sync_error",
            "platform": platform_id,
            "error": str(e),
            "timestamp": datetime.utcnow()
        })