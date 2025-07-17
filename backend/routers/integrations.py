from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.analytics import Integration, IntegrationCreate, IntegrationUpdate, PlatformMetrics
from utils.auth import verify_token
from database import get_collection
from bson import ObjectId
import random

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_integrations(current_user: str = Depends(verify_token)):
    integrations_collection = await get_collection("integrations")
    
    integrations = await integrations_collection.find({"user_email": current_user}).to_list(100)
    
    # Convert ObjectId to string
    for integration in integrations:
        integration["id"] = str(integration["_id"])
        del integration["_id"]
    
    return integrations

@router.post("/", response_model=dict)
async def create_integration(
    integration: IntegrationCreate,
    current_user: str = Depends(verify_token)
):
    integrations_collection = await get_collection("integrations")
    
    # Check if integration already exists
    existing = await integrations_collection.find_one({
        "user_email": current_user,
        "platform": integration.platform
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="Integration already exists")
    
    integration_dict = integration.dict()
    integration_dict["user_email"] = current_user
    integration_dict["is_connected"] = True
    
    result = await integrations_collection.insert_one(integration_dict)
    
    return {"message": "Integration created successfully", "id": str(result.inserted_id)}

@router.put("/{integration_id}", response_model=dict)
async def update_integration(
    integration_id: str,
    integration: IntegrationUpdate,
    current_user: str = Depends(verify_token)
):
    integrations_collection = await get_collection("integrations")
    
    update_data = {k: v for k, v in integration.dict().items() if v is not None}
    
    result = await integrations_collection.update_one(
        {"_id": ObjectId(integration_id), "user_email": current_user},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return {"message": "Integration updated successfully"}

@router.delete("/{integration_id}", response_model=dict)
async def delete_integration(
    integration_id: str,
    current_user: str = Depends(verify_token)
):
    integrations_collection = await get_collection("integrations")
    
    result = await integrations_collection.delete_one(
        {"_id": ObjectId(integration_id), "user_email": current_user}
    )
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    return {"message": "Integration deleted successfully"}

@router.post("/{integration_id}/sync", response_model=dict)
async def sync_integration(
    integration_id: str,
    current_user: str = Depends(verify_token)
):
    integrations_collection = await get_collection("integrations")
    
    integration = await integrations_collection.find_one(
        {"_id": ObjectId(integration_id), "user_email": current_user}
    )
    
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    # Mock sync process
    await integrations_collection.update_one(
        {"_id": ObjectId(integration_id)},
        {"$set": {"last_sync": datetime.utcnow()}}
    )
    
    return {"message": "Sync completed successfully"}

@router.get("/platforms/metrics", response_model=List[PlatformMetrics])
async def get_platform_metrics(current_user: str = Depends(verify_token)):
    # Mock platform metrics
    platforms = [
        PlatformMetrics(
            platform="shopify",
            revenue=75000.0,
            orders=750,
            aov=100.0,
            roas=4.5,
            spend=16666.67
        ),
        PlatformMetrics(
            platform="facebook",
            revenue=35000.0,
            orders=350,
            aov=100.0,
            roas=3.8,
            spend=9210.53
        ),
        PlatformMetrics(
            platform="google",
            revenue=15000.0,
            orders=150,
            aov=100.0,
            roas=5.2,
            spend=2884.62
        )
    ]
    
    return platforms
