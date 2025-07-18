import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "d2c_analytics")

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db = Database()

async def get_database():
    """Get database instance"""
    if db.database is None:
        await connect_to_mongo()
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    try:
        db.client = AsyncIOMotorClient(MONGODB_URL)
        db.database = db.client[DATABASE_NAME]
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info("✅ Connected to MongoDB successfully")
        
    except ConnectionFailure as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("✅ MongoDB connection closed")

async def init_database():
    """Initialize database with required collections and indexes"""
    try:
        database = await get_database()
        
        # Create collections if they don't exist
        collections = [
            "user_preferences",
            "sync_logs", 
            "platform_configs",
            "custom_charts",
            "ai_queries",
            "export_logs"
        ]
        
        existing_collections = await database.list_collection_names()
        
        for collection_name in collections:
            if collection_name not in existing_collections:
                await database.create_collection(collection_name)
                logger.info(f"✅ Created collection: {collection_name}")
        
        # Create indexes for better performance
        await create_indexes(database)
        
        # Insert default data
        await insert_default_data(database)
        
        logger.info("✅ Database initialization completed")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise e

async def create_indexes(database):
    """Create database indexes"""
    try:
        # User preferences indexes
        await database.user_preferences.create_index("user_id", unique=True)
        
        # Sync logs indexes
        await database.sync_logs.create_index([("platform", 1), ("timestamp", -1)])
        await database.sync_logs.create_index("timestamp")
        
        # Platform configs indexes
        await database.platform_configs.create_index("platform_id", unique=True)
        
        # AI queries indexes
        await database.ai_queries.create_index([("user_id", 1), ("timestamp", -1)])
        
        # Export logs indexes
        await database.export_logs.create_index([("user_id", 1), ("timestamp", -1)])
        
        logger.info("✅ Database indexes created")
        
    except Exception as e:
        logger.error(f"❌ Failed to create indexes: {e}")
        raise e

async def insert_default_data(database):
    """Insert default configuration data"""
    try:
        # Default user preferences
        default_prefs = {
            "user_id": "default",
            "selectedPlatforms": ["all"],
            "defaultTimeRange": "30d",
            "favoriteCharts": [],
            "theme": "system",
            "aiEnabled": True,
            "dashboardLayout": [],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        
        await database.user_preferences.update_one(
            {"user_id": "default"},
            {"$setOnInsert": default_prefs},
            upsert=True
        )
        
        # Default platform configurations
        platform_configs = [
            {
                "platform_id": "shopify",
                "name": "Shopify",
                "enabled": True,
                "api_config": {
                    "base_url": "https://{shop}.myshopify.com/admin/api/2023-10",
                    "required_scopes": ["read_orders", "read_customers", "read_products", "read_analytics"]
                },
                "sync_frequency": "hourly",
                "last_sync": None
            },
            {
                "platform_id": "facebook",
                "name": "Facebook Ads",
                "enabled": True,
                "api_config": {
                    "base_url": "https://graph.facebook.com/v18.0",
                    "required_permissions": ["ads_read", "ads_management"]
                },
                "sync_frequency": "hourly",
                "last_sync": None
            },
            {
                "platform_id": "google",
                "name": "Google Ads",
                "enabled": True,
                "api_config": {
                    "base_url": "https://googleads.googleapis.com/v14",
                    "required_scopes": ["https://www.googleapis.com/auth/adwords"]
                },
                "sync_frequency": "hourly",
                "last_sync": None
            },
            {
                "platform_id": "shiprocket",
                "name": "Shiprocket",
                "enabled": True,
                "api_config": {
                    "base_url": "https://apiv2.shiprocket.in/v1/external",
                    "required_permissions": ["orders", "shipments", "tracking"]
                },
                "sync_frequency": "daily",
                "last_sync": None
            }
        ]
        
        for config in platform_configs:
            await database.platform_configs.update_one(
                {"platform_id": config["platform_id"]},
                {"$setOnInsert": config},
                upsert=True
            )
        
        logger.info("✅ Default data inserted")
        
    except Exception as e:
        logger.error(f"❌ Failed to insert default data: {e}")
        raise e

# Utility functions for common database operations
async def log_sync_operation(platform: str, status: str, details: dict = None):
    """Log a sync operation"""
    try:
        database = await get_database()
        log_entry = {
            "platform": platform,
            "status": status,
            "details": details or {},
            "timestamp": asyncio.get_event_loop().time()
        }
        
        await database.sync_logs.insert_one(log_entry)
        
    except Exception as e:
        logger.error(f"Failed to log sync operation: {e}")

async def get_platform_config(platform_id: str):
    """Get platform configuration"""
    try:
        database = await get_database()
        config = await database.platform_configs.find_one({"platform_id": platform_id})
        return config
        
    except Exception as e:
        logger.error(f"Failed to get platform config: {e}")
        return None

async def update_platform_sync_time(platform_id: str):
    """Update last sync time for a platform"""
    try:
        database = await get_database()
        await database.platform_configs.update_one(
            {"platform_id": platform_id},
            {"$set": {"last_sync": asyncio.get_event_loop().time()}}
        )
        
    except Exception as e:
        logger.error(f"Failed to update sync time: {e}")

async def save_ai_query(user_id: str, query: str, response: str, sql_query: str = None):
    """Save AI query for analytics"""
    try:
        database = await get_database()
        query_log = {
            "user_id": user_id,
            "query": query,
            "response": response,
            "sql_query": sql_query,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        await database.ai_queries.insert_one(query_log)
        
    except Exception as e:
        logger.error(f"Failed to save AI query: {e}")

async def get_recent_ai_queries(user_id: str, limit: int = 10):
    """Get recent AI queries for a user"""
    try:
        database = await get_database()
        queries = await database.ai_queries.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit).to_list(length=limit)
        
        return queries
        
    except Exception as e:
        logger.error(f"Failed to get AI queries: {e}")
        return []