import asyncio
import aiohttp
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from utils.bigquery_client import BigQueryClient

logger = logging.getLogger(__name__)

class ShiprocketClient:
    def __init__(self, api_key: str = None, email: str = None, password: str = None):
        # Get credentials from environment if not provided
        self.api_key = api_key or os.getenv("SHIPROCKET_API_KEY")
        self.email = email or os.getenv("SHIPROCKET_EMAIL")
        self.password = password or os.getenv("SHIPROCKET_PASSWORD")
        self.base_url = "https://apiv2.shiprocket.in/v1/external"
        
        # Check if we have required credentials
        if not all([self.email, self.password]):
            logger.info("🔄 Running in demo mode - Shiprocket credentials not found")
            self.is_connected = False
            self.auth_token = None
        else:
            self.is_connected = True
            self.auth_token = None
            logger.info(f"✅ Shiprocket client initialized for email: {self.email}")
        
        self.bigquery_client = BigQueryClient()
    
    async def _get_auth_token(self) -> str:
        """Get authentication token"""
        try:
            if self.auth_token:
                return self.auth_token
            
            data = {
                "email": self.email,
                "password": self.password
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/auth/login",
                    json=data
                ) as response:
                    if response.status == 200:
                        auth_data = await response.json()
                        self.auth_token = auth_data.get("token")
                        return self.auth_token
                    else:
                        raise Exception(f"Failed to get auth token: HTTP {response.status}")
        except Exception as e:
            logger.error(f"Error getting auth token: {e}")
            raise e
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Shiprocket API connection"""
        if not self.is_connected:
            return {"success": False, "error": "Shiprocket client not initialized - running in demo mode"}
            
        try:
            auth_token = await self._get_auth_token()
            
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/settings/company/pickup",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        pickup_locations = data.get("data", {}).get("shipping_address", [])
                        return {
                            "success": True,
                            "message": "Shiprocket connection successful",
                            "pickup_locations": len(pickup_locations),
                            "company_info": "Connected successfully"
                        }
                    else:
                        error_data = await response.json()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_data.get('message', 'Unknown error')}"
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_shipments(self, limit: int = 100, page: int = 1, date_range: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Get shipments from Shiprocket"""
        if not self.is_connected:
            logger.info("🔄 Skipping Shiprocket shipments fetch - running in demo mode")
            return []
            
        try:
            auth_token = await self._get_auth_token()
            
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            
            params = {
                "per_page": min(limit, 100),
                "page": page
            }
            
            # Add date filter if provided
            if date_range:
                params["created_since"] = date_range.get("start_date")
                params["created_until"] = date_range.get("end_date")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/orders",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        shipments = data.get("data", [])
                        
                        # Process shipments for BigQuery
                        processed_shipments = []
                        for shipment in shipments:
                            processed_shipment = self._process_shipment(shipment)
                            processed_shipments.append(processed_shipment)
                        
                        return processed_shipments
                    else:
                        logger.error(f"Failed to get shipments: HTTP {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error getting shipments: {e}")
            return []
    
    async def get_tracking_data(self, awb: str) -> Dict[str, Any]:
        """Get tracking data for a specific AWB"""
        try:
            auth_token = await self._get_auth_token()
            
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/courier/track/awb/{awb}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("tracking_data", {})
                    else:
                        logger.error(f"Failed to get tracking data: HTTP {response.status}")
                        return {}
        except Exception as e:
            logger.error(f"Error getting tracking data: {e}")
            return {}
    
    async def get_courier_serviceability(self, pickup_postcode: str, delivery_postcode: str, weight: float) -> Dict[str, Any]:
        """Check courier serviceability"""
        try:
            auth_token = await self._get_auth_token()
            
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            
            params = {
                "pickup_postcode": pickup_postcode,
                "delivery_postcode": delivery_postcode,
                "weight": weight,
                "cod": 0  # 0 for prepaid, 1 for COD
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/courier/serviceability",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", {})
                    else:
                        logger.error(f"Failed to get serviceability: HTTP {response.status}")
                        return {}
        except Exception as e:
            logger.error(f"Error getting serviceability: {e}")
            return {}
    
    async def sync_to_bigquery(self, force_refresh: bool = False, date_range: Optional[Dict[str, str]] = None):
        """Sync all Shiprocket data to BigQuery"""
        try:
            logger.info("🔄 Starting Shiprocket data sync to BigQuery...")
            
            # Determine date range for sync
            if not date_range:
                if force_refresh:
                    # Get last 90 days for full refresh
                    end_date = datetime.utcnow().date()
                    start_date = end_date - timedelta(days=90)
                else:
                    # Get last 7 days for incremental sync
                    end_date = datetime.utcnow().date()
                    start_date = end_date - timedelta(days=7)
                
                date_range = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
            
            # Sync shipments
            await self._sync_shipments_to_bigquery(date_range)
            
            logger.info("✅ Shiprocket data sync completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Shiprocket sync failed: {e}")
            raise e
    
    async def _sync_shipments_to_bigquery(self, date_range: Dict[str, str]):
        """Sync shipments to BigQuery"""
        try:
            all_shipments = []
            page = 1
            
            while True:
                shipments = await self.get_shipments(limit=100, page=page, date_range=date_range)
                
                if not shipments:
                    break
                
                all_shipments.extend(shipments)
                
                # Rate limiting
                await asyncio.sleep(1)
                
                # Break if we got less than the limit (last page)
                if len(shipments) < 100:
                    break
                
                page += 1
            
            if all_shipments:
                await self.bigquery_client.insert_data("shiprocket_shipments", all_shipments)
                logger.info(f"✅ Synced {len(all_shipments)} Shiprocket shipments to BigQuery")
            
        except Exception as e:
            logger.error(f"❌ Failed to sync Shiprocket shipments: {e}")
            raise e
    
    def _process_shipment(self, shipment: Dict[str, Any]) -> Dict[str, Any]:
        """Process shipment data for BigQuery"""
        # Extract shipment details
        shipment_id = str(shipment.get("id", ""))
        order_id = str(shipment.get("order_id", ""))
        
        # Get AWB and courier info
        awb = shipment.get("awb", "")
        courier_name = shipment.get("courier_name", "")
        
        # Get status and dates
        status = shipment.get("status", "")
        pickup_date = shipment.get("pickup_scheduled_date", "")
        delivered_date = shipment.get("delivered_date", "")
        expected_delivery = shipment.get("expected_delivery_date", "")
        
        # Get charges
        shipping_charges = float(shipment.get("shipping_charges", 0))
        cod_charges = float(shipment.get("cod_charges", 0))
        
        # Get dimensions
        weight = float(shipment.get("weight", 0))
        length = float(shipment.get("length", 0))
        breadth = float(shipment.get("breadth", 0))
        height = float(shipment.get("height", 0))
        
        # Get addresses
        pickup_address = shipment.get("pickup_location", {})
        delivery_address = shipment.get("delivery_address", {})
        
        return {
            "shipment_id": shipment_id,
            "order_id": order_id,
            "awb": awb,
            "courier_name": courier_name,
            "status": status,
            "pickup_date": pickup_date if pickup_date else None,
            "delivered_date": delivered_date if delivered_date else None,
            "expected_delivery_date": expected_delivery if expected_delivery else None,
            "shipping_charges": shipping_charges,
            "cod_charges": cod_charges,
            "weight": weight,
            "length": length,
            "breadth": breadth,
            "height": height,
            "pickup_address": json.dumps(pickup_address) if pickup_address else None,
            "delivery_address": json.dumps(delivery_address) if delivery_address else None,
            "tracking_data": json.dumps({}),  # Will be populated separately
            "platform": "shiprocket"
        }