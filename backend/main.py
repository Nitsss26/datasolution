from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from datetime import datetime, timedelta
import asyncio
import uvicorn

# Import our custom modules
from database import get_database, init_database
from models.analytics import AnalyticsData, PlatformData, UserPreferences
from routers import shopify
from routers import facebook_ads  
from routers import google_ads
from routers import shiprocket
from routers import analytics
from routers import ai_insights
from routers import integrations
from routers import demo_data
from routers import pipeline
from routers import auth
from routers import comprehensive_analytics
from utils.bigquery_client import BigQueryClient
from utils.data_processor import DataProcessor
from utils.scheduler import DataScheduler

app = FastAPI(
    title="D2C Analytics API",
    description="Comprehensive D2C Analytics Platform with AI-powered insights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",
        "http://82.29.164.244:3000",
        "http://82.29.164.244:3001",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
bigquery_client = BigQueryClient()
data_processor = DataProcessor(bigquery_client)
scheduler = DataScheduler(data_processor)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]

class DataSyncRequest(BaseModel):
    platforms: List[str]
    force_refresh: bool = False

class AnalyticsRequest(BaseModel):
    platforms: List[str] = ["all"]
    time_range: str = "30d"
    metrics: Optional[List[str]] = None
    granularity: str = "daily"

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks"""
    try:
        await init_database()
        print("✅ Database initialized successfully")
        
        # Initialize BigQuery tables
        await bigquery_client.init_tables()
        print("✅ BigQuery tables initialized")
        
        # Start data sync scheduler
        scheduler.start()
        print("✅ Data sync scheduler started")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services = {
        "database": "healthy",
        "bigquery": "healthy" if bigquery_client and hasattr(bigquery_client, 'is_connected') and bigquery_client.is_connected() else "demo_mode",
        "scheduler": "running" if scheduler and hasattr(scheduler, 'is_running') and scheduler.is_running else "stopped"
    }
    
    return HealthResponse(
        status="healthy" if all(s == "healthy" or s == "running" for s in services.values()) else "degraded",
        timestamp=datetime.utcnow().isoformat(),
        services=services
    )

# Data sync endpoint
@app.post("/api/sync")
async def sync_data(request: DataSyncRequest, background_tasks: BackgroundTasks):
    """Trigger data synchronization for specified platforms"""
    try:
        # Add background task for data sync
        background_tasks.add_task(
            data_processor.sync_all_platforms,
            platforms=request.platforms,
            force_refresh=request.force_refresh
        )
        
        return {
            "message": "Data sync initiated",
            "platforms": request.platforms,
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

# Main analytics endpoint
@app.post("/api/analytics")
async def get_analytics(request: AnalyticsRequest):
    """Get comprehensive analytics data"""
    try:
        # Process the request
        analytics_data = await data_processor.get_analytics(
            platforms=request.platforms,
            time_range=request.time_range,
            metrics=request.metrics,
            granularity=request.granularity
        )
        
        return analytics_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics fetch failed: {str(e)}")

# Platform status endpoint
@app.get("/api/platforms/status")
async def get_platform_status():
    """Get connection status for all platforms"""
    try:
        platforms = [
            {
                "id": "shopify",
                "name": "Shopify",
                "connected": await check_shopify_connection(),
                "last_sync": await get_last_sync_time("shopify"),
                "data_points": await get_data_count("shopify")
            },
            {
                "id": "facebook",
                "name": "Facebook Ads",
                "connected": await check_facebook_connection(),
                "last_sync": await get_last_sync_time("facebook"),
                "data_points": await get_data_count("facebook")
            },
            {
                "id": "google",
                "name": "Google Ads",
                "connected": await check_google_connection(),
                "last_sync": await get_last_sync_time("google"),
                "data_points": await get_data_count("google")
            },
            {
                "id": "shiprocket",
                "name": "Shiprocket",
                "connected": await check_shiprocket_connection(),
                "last_sync": await get_last_sync_time("shiprocket"),
                "data_points": await get_data_count("shiprocket")
            }
        ]
        
        return {"platforms": platforms}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Platform status fetch failed: {str(e)}")

# User preferences endpoints
@app.get("/api/user/preferences")
async def get_user_preferences():
    """Get user preferences"""
    try:
        db = await get_database()
        prefs = await db.user_preferences.find_one({"user_id": "default"})
        
        if not prefs:
            # Return default preferences
            return {
                "selectedPlatforms": ["all"],
                "defaultTimeRange": "30d",
                "favoriteCharts": [],
                "theme": "system",
                "aiEnabled": True,
                "dashboardLayout": []
            }
        
        return prefs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preferences fetch failed: {str(e)}")

@app.post("/api/user/preferences")
async def save_user_preferences(preferences: Dict[str, Any]):
    """Save user preferences"""
    try:
        db = await get_database()
        await db.user_preferences.update_one(
            {"user_id": "default"},
            {"$set": {**preferences, "updated_at": datetime.utcnow()}},
            upsert=True
        )
        
        return {"message": "Preferences saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preferences save failed: {str(e)}")

# Include routers
app.include_router(shopify.router, prefix="/api/shopify", tags=["Shopify"])
app.include_router(facebook_ads.router, prefix="/api/facebook", tags=["Facebook Ads"])
app.include_router(google_ads.router, prefix="/api/google", tags=["Google Ads"])
app.include_router(shiprocket.router, prefix="/api/shiprocket", tags=["Shiprocket"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(comprehensive_analytics.router, prefix="/api/comprehensive", tags=["Comprehensive Analytics"])
app.include_router(ai_insights.router, prefix="/api/ai", tags=["AI Insights"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrations"])
app.include_router(demo_data.router, prefix="/api/demo", tags=["Demo Data"])
app.include_router(pipeline.router, prefix="/api/pipeline", tags=["Pipeline Control"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Helper functions
async def check_shopify_connection() -> bool:
    """Check if Shopify is connected"""
    try:
        # Implement actual connection check
        return os.getenv("SHOPIFY_API_KEY") is not None
    except:
        return False

async def check_facebook_connection() -> bool:
    """Check if Facebook Ads is connected"""
    try:
        return os.getenv("FACEBOOK_ACCESS_TOKEN") is not None
    except:
        return False

async def check_google_connection() -> bool:
    """Check if Google Ads is connected"""
    try:
        return os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN") is not None
    except:
        return False

async def check_shiprocket_connection() -> bool:
    """Check if Shiprocket is connected"""
    try:
        return os.getenv("SHIPROCKET_API_KEY") is not None
    except:
        return False

async def get_last_sync_time(platform: str) -> Optional[str]:
    """Get last sync time for a platform"""
    try:
        db = await get_database()
        sync_log = await db.sync_logs.find_one(
            {"platform": platform},
            sort=[("timestamp", -1)]
        )
        return sync_log["timestamp"].isoformat() if sync_log else None
    except:
        return None

async def get_data_count(platform: str) -> int:
    """Get data point count for a platform"""
    try:
        # Query BigQuery for data count
        count = await bigquery_client.get_data_count(platform)
        return count
    except:
        return 0

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )