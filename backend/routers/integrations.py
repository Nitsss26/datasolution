from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.analytics import IntegrationConfig, Platform
from utils.auth import verify_token
from database import get_database
from integrations.shopify_client import ShopifyClient
from integrations.facebook_ads_client import FacebookAdsClient
from integrations.google_ads_client import GoogleAdsClient
from integrations.shiprocket_client import ShiprocketClient

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_integrations(current_user: str = Depends(verify_token)):
    """Get all integrations for the current user"""
    db = await get_database()
    user = await db.users.find_one({"email": current_user})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    integrations = await db.integrations.find({"user_email": current_user}).to_list(100)
    
    # Convert ObjectId to string and remove sensitive data
    for integration in integrations:
        integration["_id"] = str(integration["_id"])
        integration.pop("api_key", None)  # Don't expose API keys
    
    return integrations

@router.post("/connect")
async def connect_integration(
    platform: Platform,
    api_key: str,
    additional_config: dict = {},
    current_user: str = Depends(verify_token)
):
    """Connect a new integration"""
    db = await get_database()
    
    # Test the connection based on platform
    try:
        if platform == Platform.SHOPIFY:
            client = ShopifyClient(api_key, additional_config.get("shop_domain"))
            await client.test_connection()
        elif platform == Platform.FACEBOOK_ADS:
            client = FacebookAdsClient(api_key)
            await client.test_connection()
        elif platform == Platform.GOOGLE_ADS:
            client = GoogleAdsClient(api_key, additional_config)
            await client.test_connection()
        elif platform == Platform.SHIPROCKET:
            client = ShiprocketClient(api_key)
            await client.test_connection()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to connect to {platform.value}: {str(e)}"
        )
    
    # Save integration
    integration_data = {
        "user_email": current_user,
        "platform": platform.value,
        "api_key": api_key,
        "additional_config": additional_config,
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    # Check if integration already exists
    existing = await db.integrations.find_one({
        "user_email": current_user,
        "platform": platform.value
    })
    
    if existing:
        # Update existing integration
        await db.integrations.update_one(
            {"_id": existing["_id"]},
            {"$set": integration_data}
        )
        return {"message": f"{platform.value} integration updated successfully"}
    else:
        # Create new integration
        result = await db.integrations.insert_one(integration_data)
        return {"message": f"{platform.value} integration connected successfully", "id": str(result.inserted_id)}

@router.delete("/{platform}")
async def disconnect_integration(
    platform: Platform,
    current_user: str = Depends(verify_token)
):
    """Disconnect an integration"""
    db = await get_database()
    
    result = await db.integrations.delete_one({
        "user_email": current_user,
        "platform": platform.value
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    return {"message": f"{platform.value} integration disconnected successfully"}

@router.post("/sync/{platform}")
async def sync_platform_data(
    platform: Platform,
    current_user: str = Depends(verify_token)
):
    """Manually sync data from a specific platform"""
    db = await get_database()
    
    # Get integration config
    integration = await db.integrations.find_one({
        "user_email": current_user,
        "platform": platform.value
    })
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    try:
        # Sync data based on platform
        if platform == Platform.SHOPIFY:
            client = ShopifyClient(integration["api_key"], integration["additional_config"].get("shop_domain"))
            data = await client.fetch_data()
        elif platform == Platform.FACEBOOK_ADS:
            client = FacebookAdsClient(integration["api_key"])
            data = await client.fetch_data()
        elif platform == Platform.GOOGLE_ADS:
            client = GoogleAdsClient(integration["api_key"], integration["additional_config"])
            data = await client.fetch_data()
        elif platform == Platform.SHIPROCKET:
            client = ShiprocketClient(integration["api_key"])
            data = await client.fetch_data()
        
        # Store data in database (implement based on your data structure)
        # await store_platform_data(current_user, platform, data)
        
        return {"message": f"Data synced successfully from {platform.value}", "records": len(data)}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync data: {str(e)}"
        )
