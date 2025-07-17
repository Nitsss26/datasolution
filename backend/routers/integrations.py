from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from models.analytics import IntegrationCreate, IntegrationResponse
from utils.auth import verify_token
from database import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_data = await verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return token_data

@router.get("/", response_model=List[IntegrationResponse])
async def get_integrations(current_user: dict = Depends(get_current_user)):
    """Get all integrations for current user"""
    db = get_database()
    
    # Get user
    user = await db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get integrations
    integrations = await db.integrations.find({"user_id": str(user["_id"])}).to_list(100)
    
    result = []
    for integration in integrations:
        result.append({
            "id": str(integration["_id"]),
            "platform": integration["platform"],
            "is_active": integration.get("is_active", True),
            "created_at": integration.get("created_at", datetime.utcnow()),
            "last_sync": integration.get("last_sync")
        })
    
    return result

@router.post("/", response_model=dict)
async def create_integration(
    integration: IntegrationCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new integration"""
    db = get_database()
    
    # Get user
    user = await db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if integration already exists
    existing = await db.integrations.find_one({
        "user_id": str(user["_id"]),
        "platform": integration.platform
    })
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Integration with {integration.platform} already exists"
        )
    
    # Create integration
    integration_data = {
        "user_id": str(user["_id"]),
        "platform": integration.platform,
        "credentials": integration.credentials,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "last_sync": None
    }
    
    result = await db.integrations.insert_one(integration_data)
    
    return {
        "message": f"{integration.platform} integration created successfully",
        "integration_id": str(result.inserted_id)
    }

@router.post("/{integration_id}/sync")
async def sync_integration(
    integration_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Sync data from integration"""
    db = get_database()
    
    # Get user
    user = await db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get integration
    try:
        integration = await db.integrations.find_one({
            "_id": ObjectId(integration_id),
            "user_id": str(user["_id"])
        })
    except:
        raise HTTPException(status_code=400, detail="Invalid integration ID")
    
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    # Update last sync time
    await db.integrations.update_one(
        {"_id": ObjectId(integration_id)},
        {"$set": {"last_sync": datetime.utcnow()}}
    )
    
    return {
        "message": f"{integration['platform']} data synced successfully",
        "synced_at": datetime.utcnow().isoformat()
    }

@router.delete("/{integration_id}")
async def delete_integration(
    integration_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete integration"""
    db = get_database()
    
    # Get user
    user = await db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete integration
    try:
        result = await db.integrations.delete_one({
            "_id": ObjectId(integration_id),
            "user_id": str(user["_id"])
        })
    except:
        raise HTTPException(status_code=400, detail="Invalid integration ID")
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return {"message": "Integration deleted successfully"}

@router.get("/available")
async def get_available_integrations():
    """Get list of available integrations"""
    return {
        "integrations": [
            {
                "platform": "shopify",
                "name": "Shopify",
                "description": "Connect your Shopify store for sales and inventory data",
                "fields": [
                    {"name": "shop_url", "label": "Shop URL", "type": "text", "required": True},
                    {"name": "access_token", "label": "Access Token", "type": "password", "required": True}
                ]
            },
            {
                "platform": "facebook_ads",
                "name": "Facebook Ads",
                "description": "Connect Facebook Ads for advertising performance data",
                "fields": [
                    {"name": "access_token", "label": "Access Token", "type": "password", "required": True},
                    {"name": "ad_account_id", "label": "Ad Account ID", "type": "text", "required": True}
                ]
            },
            {
                "platform": "google_ads",
                "name": "Google Ads",
                "description": "Connect Google Ads for search advertising data",
                "fields": [
                    {"name": "customer_id", "label": "Customer ID", "type": "text", "required": True},
                    {"name": "developer_token", "label": "Developer Token", "type": "password", "required": True}
                ]
            },
            {
                "platform": "shiprocket",
                "name": "Shiprocket",
                "description": "Connect Shiprocket for shipping and logistics data",
                "fields": [
                    {"name": "email", "label": "Email", "type": "email", "required": True},
                    {"name": "password", "label": "Password", "type": "password", "required": True}
                ]
            }
        ]
    }
