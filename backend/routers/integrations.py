from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from models.analytics import Integration
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_integrations():
    # Mock data - replace with actual database queries
    return {
        "integrations": [
            {
                "id": "1",
                "platform": "shopify",
                "platform_name": "Shopify",
                "status": "connected",
                "last_sync": "2024-01-15T10:30:00Z"
            },
            {
                "id": "2",
                "platform": "facebook_ads",
                "platform_name": "Facebook Ads",
                "status": "connected",
                "last_sync": "2024-01-15T09:15:00Z"
            },
            {
                "id": "3",
                "platform": "google_ads",
                "platform_name": "Google Ads",
                "status": "disconnected",
                "last_sync": None
            },
            {
                "id": "4",
                "platform": "shiprocket",
                "platform_name": "Shiprocket",
                "status": "connected",
                "last_sync": "2024-01-15T08:45:00Z"
            }
        ]
    }

@router.get("/available")
async def get_available_integrations():
    return {
        "platforms": [
            {
                "id": "shopify",
                "name": "Shopify",
                "description": "Connect your Shopify store to sync orders, products, and customer data",
                "icon": "shopify",
                "category": "ecommerce"
            },
            {
                "id": "facebook_ads",
                "name": "Facebook Ads",
                "description": "Track your Facebook advertising performance and ROAS",
                "icon": "facebook",
                "category": "advertising"
            },
            {
                "id": "google_ads",
                "name": "Google Ads",
                "description": "Monitor Google Ads campaigns and keyword performance",
                "icon": "google",
                "category": "advertising"
            },
            {
                "id": "shiprocket",
                "name": "Shiprocket",
                "description": "Track shipping and delivery metrics",
                "icon": "shiprocket",
                "category": "logistics"
            },
            {
                "id": "amazon",
                "name": "Amazon Seller Central",
                "description": "Sync Amazon marketplace data and performance metrics",
                "icon": "amazon",
                "category": "marketplace"
            },
            {
                "id": "flipkart",
                "name": "Flipkart Seller Hub",
                "description": "Connect Flipkart seller account for marketplace analytics",
                "icon": "flipkart",
                "category": "marketplace"
            }
        ]
    }

@router.post("/connect")
async def connect_integration(integration_data: Dict[str, Any]):
    platform = integration_data.get("platform")
    credentials = integration_data.get("credentials", {})
    
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Platform is required"
        )
    
    # Mock connection - replace with actual integration logic
    return {
        "message": f"Successfully connected to {platform}",
        "status": "connected",
        "platform": platform
    }

@router.post("/{integration_id}/sync")
async def sync_integration(integration_id: str):
    # Mock sync - replace with actual sync logic
    return {
        "message": "Sync completed successfully",
        "last_sync": datetime.utcnow().isoformat(),
        "records_synced": 150
    }

@router.delete("/{integration_id}")
async def disconnect_integration(integration_id: str):
    # Mock disconnect - replace with actual disconnect logic
    return {
        "message": "Integration disconnected successfully"
    }
