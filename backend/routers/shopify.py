from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from ..integrations.shopify_client import ShopifyClient
from ..database import log_sync_operation, update_platform_sync_time

logger = logging.getLogger(__name__)

router = APIRouter()
shopify_client = ShopifyClient()

class SyncRequest(BaseModel):
    force_refresh: bool = False
    date_range: Optional[str] = None

@router.get("/status")
async def get_shopify_status():
    """Get Shopify connection status"""
    try:
        is_connected = await shopify_client.test_connection()
        shop_info = await shopify_client.get_shop_info() if is_connected else None
        
        return {
            "platform": "shopify",
            "connected": is_connected,
            "shop_info": shop_info,
            "currency": "INR",
            "last_check": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Shopify status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@router.post("/sync")
async def sync_shopify_data(request: SyncRequest, background_tasks: BackgroundTasks):
    """Trigger Shopify data synchronization"""
    try:
        # Log sync start
        await log_sync_operation("shopify", "started", {"force_refresh": request.force_refresh})
        
        # Add background task for data sync
        background_tasks.add_task(
            sync_shopify_background,
            force_refresh=request.force_refresh,
            date_range=request.date_range
        )
        
        return {
            "message": "Shopify data sync initiated",
            "status": "processing",
            "platform": "shopify"
        }
        
    except Exception as e:
        logger.error(f"Shopify sync failed: {e}")
        await log_sync_operation("shopify", "failed", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

async def sync_shopify_background(force_refresh: bool = False, date_range: str = None):
    """Background task for Shopify data sync"""
    try:
        logger.info("🔄 Starting Shopify background sync")
        
        # Get orders
        orders = await shopify_client.get_orders(limit=250)
        logger.info(f"Retrieved {len(orders)} orders")
        
        # Get customers
        customers = await shopify_client.get_customers(limit=250)
        logger.info(f"Retrieved {len(customers)} customers")
        
        # Get products
        products = await shopify_client.get_products(limit=250)
        logger.info(f"Retrieved {len(products)} products")
        
        # Update sync time
        await update_platform_sync_time("shopify")
        
        # Log success
        await log_sync_operation("shopify", "completed", {
            "orders_count": len(orders),
            "customers_count": len(customers),
            "products_count": len(products)
        })
        
        logger.info("✅ Shopify background sync completed")
        
    except Exception as e:
        logger.error(f"❌ Shopify background sync failed: {e}")
        await log_sync_operation("shopify", "failed", {"error": str(e)})

@router.get("/orders")
async def get_shopify_orders(limit: int = 50, status: str = "any"):
    """Get Shopify orders"""
    try:
        orders = await shopify_client.get_orders(limit=limit, status=status)
        
        # Convert to INR if needed and add metadata
        processed_orders = []
        for order in orders:
            processed_order = {
                **order,
                "currency_display": "INR",
                "total_price_inr": float(order.get("total_price", 0)),
                "subtotal_price_inr": float(order.get("subtotal_price", 0)),
                "total_tax_inr": float(order.get("total_tax", 0))
            }
            processed_orders.append(processed_order)
        
        return {
            "orders": processed_orders,
            "count": len(processed_orders),
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get orders failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get orders failed: {str(e)}")

@router.get("/customers")
async def get_shopify_customers(limit: int = 50):
    """Get Shopify customers"""
    try:
        customers = await shopify_client.get_customers(limit=limit)
        
        # Add INR formatting
        processed_customers = []
        for customer in customers:
            processed_customer = {
                **customer,
                "currency_display": "INR",
                "total_spent_inr": float(customer.get("total_spent", 0))
            }
            processed_customers.append(processed_customer)
        
        return {
            "customers": processed_customers,
            "count": len(processed_customers),
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get customers failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get customers failed: {str(e)}")

@router.get("/products")
async def get_shopify_products(limit: int = 50):
    """Get Shopify products"""
    try:
        products = await shopify_client.get_products(limit=limit)
        
        return {
            "products": products,
            "count": len(products),
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Get products failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get products failed: {str(e)}")

@router.get("/analytics")
async def get_shopify_analytics(date_range: str = "last_30_days"):
    """Get Shopify analytics summary"""
    try:
        analytics = await shopify_client.get_analytics_data(date_range)
        
        # Ensure all amounts are in INR
        if analytics:
            analytics["currency"] = "INR"
            analytics["total_revenue_inr"] = analytics.get("total_revenue", 0)
            analytics["average_order_value_inr"] = analytics.get("average_order_value", 0)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Get analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get analytics failed: {str(e)}")

@router.get("/test-connection")
async def test_shopify_connection():
    """Test Shopify API connection"""
    try:
        is_connected = await shopify_client.test_connection()
        
        return {
            "platform": "shopify",
            "connected": is_connected,
            "message": "Connection successful" if is_connected else "Connection failed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")