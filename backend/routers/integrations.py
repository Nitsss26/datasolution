from fastapi import APIRouter, HTTPException, Depends
from models.user import UserIntegration
from database import get_database
from datetime import datetime
from integrations.shopify_client import ShopifyClient
from integrations.facebook_ads_client import FacebookAdsClient
from integrations.google_ads_client import GoogleAdsClient
from integrations.shiprocket_client import ShiprocketClient

router = APIRouter()

@router.post("/connect/{platform}")
async def connect_integration(
    platform: str,
    credentials: dict,
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    db = await get_database()
    
    # Validate platform
    valid_platforms = ["shopify", "facebook_ads", "google_ads", "shiprocket"]
    if platform not in valid_platforms:
        raise HTTPException(status_code=400, detail="Invalid platform")
    
    # Test connection based on platform
    try:
        if platform == "shopify":
            client = ShopifyClient(credentials)
            await client.test_connection()
        elif platform == "facebook_ads":
            client = FacebookAdsClient(credentials)
            await client.test_connection()
        elif platform == "google_ads":
            client = GoogleAdsClient(credentials)
            await client.test_connection()
        elif platform == "shiprocket":
            client = ShiprocketClient(credentials)
            await client.test_connection()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Connection failed: {str(e)}")
    
    # Save or update integration
    integration_data = {
        "user_id": str(current_user["_id"]),
        "platform": platform,
        "credentials": credentials,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_sync": None
    }
    
    await db.user_integrations.update_one(
        {"user_id": str(current_user["_id"]), "platform": platform},
        {"$set": integration_data},
        upsert=True
    )
    
    return {"message": f"{platform} connected successfully"}

@router.get("/")
async def get_integrations(
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    db = await get_database()
    
    integrations = []
    async for doc in db.user_integrations.find({"user_id": str(current_user["_id"])}):
        integrations.append({
            "platform": doc["platform"],
            "is_active": doc["is_active"],
            "created_at": doc["created_at"],
            "last_sync": doc.get("last_sync")
        })
    
    return integrations

@router.post("/sync/{platform}")
async def sync_platform_data(
    platform: str,
    current_user: dict = Depends(lambda: {"_id": "user123"})  # Mock user
):
    db = await get_database()
    
    # Get integration
    integration = await db.user_integrations.find_one({
        "user_id": str(current_user["_id"]),
        "platform": platform
    })
    
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    # Sync data based on platform
    try:
        if platform == "shopify":
            client = ShopifyClient(integration["credentials"])
            data = await client.fetch_data()
        elif platform == "facebook_ads":
            client = FacebookAdsClient(integration["credentials"])
            data = await client.fetch_data()
        elif platform == "google_ads":
            client = GoogleAdsClient(integration["credentials"])
            data = await client.fetch_data()
        elif platform == "shiprocket":
            client = ShiprocketClient(integration["credentials"])
            data = await client.fetch_data()
        
        # Save analytics data
        analytics_data = {
            "user_id": str(current_user["_id"]),
            "platform": platform,
            "date": datetime.utcnow(),
            "metrics": data["metrics"],
            "raw_data": data.get("raw_data")
        }
        
        await db.analytics_data.insert_one(analytics_data)
        
        # Update last sync
        await db.user_integrations.update_one(
            {"user_id": str(current_user["_id"]), "platform": platform},
            {"$set": {"last_sync": datetime.utcnow()}}
        )
        
        return {"message": f"{platform} data synced successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")
