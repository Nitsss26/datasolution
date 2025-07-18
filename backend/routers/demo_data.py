from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import random
from datetime import datetime, timedelta
import json
import logging
from utils.bigquery_client import BigQueryClient

logger = logging.getLogger(__name__)
router = APIRouter()

class DemoDataRequest(BaseModel):
    volume: str = "medium"  # small, medium, large
    time_range: str = "30d"  # 30d, 90d, 1y

@router.post("/generate-shopify")
async def generate_shopify_demo_data(request: DemoDataRequest = DemoDataRequest()):
    """Generate dummy Shopify data"""
    try:
        bigquery_client = BigQueryClient()
        
        # Determine data volume
        volume_config = {
            "small": {"orders": 1000, "customers": 100, "products": 50},
            "medium": {"orders": 10000, "customers": 1000, "products": 200},
            "large": {"orders": 100000, "customers": 10000, "products": 500}
        }
        
        config = volume_config.get(request.volume, volume_config["medium"])
        
        # Generate dummy orders
        orders = []
        for i in range(config["orders"]):
            order_date = datetime.utcnow() - timedelta(days=random.randint(0, 90))
            order = {
                "id": f"shopify_order_{i+1}",
                "order_number": str(1000 + i),
                "created_at": order_date.isoformat(),
                "updated_at": order_date.isoformat(),
                "total_price": round(random.uniform(25.0, 500.0), 2),
                "subtotal_price": round(random.uniform(20.0, 450.0), 2),
                "total_tax": round(random.uniform(2.0, 50.0), 2),
                "currency": "INR",
                "financial_status": random.choice(["paid", "pending", "refunded"]),
                "fulfillment_status": random.choice(["fulfilled", "partial", "unfulfilled"]),
                "customer_id": f"customer_{random.randint(1, config['customers'])}",
                "email": f"customer{random.randint(1, config['customers'])}@example.com",
                "phone": f"+91{random.randint(7000000000, 9999999999)}",
                "billing_address": json.dumps({
                    "city": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]),
                    "country": "India",
                    "zip": f"{random.randint(100000, 999999)}"
                }),
                "shipping_address": json.dumps({
                    "city": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]),
                    "country": "India",
                    "zip": f"{random.randint(100000, 999999)}"
                }),
                "line_items": json.dumps([{
                    "product_id": f"product_{random.randint(1, config['products'])}",
                    "quantity": random.randint(1, 5),
                    "price": round(random.uniform(10.0, 200.0), 2)
                }]),
                "tags": random.choice(["vip", "new-customer", "repeat-customer", ""]),
                "source_name": random.choice(["web", "mobile", "pos"]),
                "referring_site": random.choice(["google.com", "facebook.com", "instagram.com", ""]),
                "landing_site": "/",
                "platform": "shopify"
            }
            orders.append(order)
        
        # Generate dummy customers
        customers = []
        for i in range(config["customers"]):
            customer_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
            customer = {
                "id": f"customer_{i+1}",
                "email": f"customer{i+1}@example.com",
                "first_name": f"Customer{i+1}",
                "last_name": "Demo",
                "phone": f"+91{random.randint(7000000000, 9999999999)}",
                "created_at": customer_date.isoformat(),
                "updated_at": customer_date.isoformat(),
                "orders_count": random.randint(1, 10),
                "total_spent": round(random.uniform(100.0, 5000.0), 2),
                "state": random.choice(["enabled", "disabled"]),
                "tags": random.choice(["vip", "regular", "new"]),
                "accepts_marketing": random.choice([True, False]),
                "addresses": json.dumps([{
                    "city": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]),
                    "country": "India",
                    "zip": f"{random.randint(100000, 999999)}"
                }]),
                "default_address": json.dumps({
                    "city": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]),
                    "country": "India",
                    "zip": f"{random.randint(100000, 999999)}"
                }),
                "platform": "shopify"
            }
            customers.append(customer)
        
        # Generate dummy products
        products = []
        product_names = ["T-Shirt", "Jeans", "Sneakers", "Backpack", "Watch", "Sunglasses", "Jacket", "Dress"]
        for i in range(config["products"]):
            product_date = datetime.utcnow() - timedelta(days=random.randint(0, 180))
            product = {
                "id": f"product_{i+1}",
                "title": f"{random.choice(product_names)} {i+1}",
                "handle": f"product-{i+1}",
                "product_type": random.choice(["Clothing", "Accessories", "Electronics", "Home"]),
                "vendor": random.choice(["Brand A", "Brand B", "Brand C"]),
                "created_at": product_date.isoformat(),
                "updated_at": product_date.isoformat(),
                "published_at": product_date.isoformat(),
                "status": "active",
                "tags": random.choice(["bestseller", "new-arrival", "sale"]),
                "variants": json.dumps([{
                    "id": f"variant_{i+1}",
                    "price": round(random.uniform(20.0, 300.0), 2),
                    "inventory_quantity": random.randint(0, 100)
                }]),
                "images": json.dumps([{
                    "src": f"https://example.com/product{i+1}.jpg"
                }]),
                "options": json.dumps([{
                    "name": "Size",
                    "values": ["S", "M", "L", "XL"]
                }]),
                "platform": "shopify"
            }
            products.append(product)
        
        # Insert data into BigQuery
        await bigquery_client.insert_data("shopify_orders", orders)
        await bigquery_client.insert_data("shopify_customers", customers)
        await bigquery_client.insert_data("shopify_products", products)
        
        return {
            "message": "Shopify demo data generated successfully",
            "data": {
                "orders": len(orders),
                "customers": len(customers),
                "products": len(products)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate Shopify demo data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-facebook")
async def generate_facebook_demo_data(request: DemoDataRequest = DemoDataRequest()):
    """Generate dummy Facebook Ads data"""
    try:
        bigquery_client = BigQueryClient()
        
        # Generate dummy Facebook campaigns
        campaigns = []
        campaign_names = ["Summer Sale", "Brand Awareness", "Product Launch", "Retargeting", "Holiday Special"]
        
        for i in range(20):  # 20 campaigns
            for days_back in range(30):  # 30 days of data
                date = (datetime.utcnow() - timedelta(days=days_back)).date()
                
                impressions = random.randint(1000, 50000)
                clicks = random.randint(50, 2000)
                spend = round(random.uniform(100.0, 5000.0), 2)
                conversions = random.randint(5, 100)
                conversion_value = round(conversions * random.uniform(50.0, 300.0), 2)
                
                campaign = {
                    "campaign_id": f"fb_campaign_{i+1}",
                    "campaign_name": f"{random.choice(campaign_names)} {i+1}",
                    "account_id": "act_123456789",
                    "date_start": date.strftime("%Y-%m-%d"),
                    "date_stop": date.strftime("%Y-%m-%d"),
                    "impressions": impressions,
                    "clicks": clicks,
                    "spend": spend,
                    "reach": random.randint(800, 40000),
                    "frequency": round(random.uniform(1.1, 3.5), 2),
                    "cpm": round((spend / impressions) * 1000, 2),
                    "cpc": round(spend / clicks, 2) if clicks > 0 else 0,
                    "ctr": round((clicks / impressions) * 100, 2) if impressions > 0 else 0,
                    "conversions": conversions,
                    "conversion_value": conversion_value,
                    "cost_per_conversion": round(spend / conversions, 2) if conversions > 0 else 0,
                    "roas": round(conversion_value / spend, 2) if spend > 0 else 0,
                    "objective": random.choice(["CONVERSIONS", "TRAFFIC", "REACH", "BRAND_AWARENESS"]),
                    "status": random.choice(["ACTIVE", "PAUSED"]),
                    "platform": "facebook"
                }
                campaigns.append(campaign)
        
        await bigquery_client.insert_data("facebook_campaigns", campaigns)
        
        return {
            "message": "Facebook Ads demo data generated successfully",
            "data": {
                "campaigns": len(campaigns)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate Facebook demo data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-google")
async def generate_google_demo_data(request: DemoDataRequest = DemoDataRequest()):
    """Generate dummy Google Ads data"""
    try:
        bigquery_client = BigQueryClient()
        
        # Generate dummy Google campaigns
        campaigns = []
        campaign_names = ["Search Campaign", "Display Campaign", "Shopping Campaign", "Video Campaign", "App Campaign"]
        
        for i in range(15):  # 15 campaigns
            for days_back in range(30):  # 30 days of data
                date = (datetime.utcnow() - timedelta(days=days_back)).date()
                
                impressions = random.randint(500, 30000)
                clicks = random.randint(25, 1500)
                cost_micros = random.randint(50000000, 3000000000)  # Cost in micros
                conversions = round(random.uniform(2.0, 80.0), 1)
                conversion_value = round(conversions * random.uniform(40.0, 250.0), 2)
                
                campaign = {
                    "campaign_id": f"google_campaign_{i+1}",
                    "campaign_name": f"{random.choice(campaign_names)} {i+1}",
                    "customer_id": "1234567890",
                    "date": date.strftime("%Y-%m-%d"),
                    "impressions": impressions,
                    "clicks": clicks,
                    "cost": cost_micros,
                    "conversions": conversions,
                    "conversion_value": conversion_value,
                    "ctr": round((clicks / impressions) * 100, 2) if impressions > 0 else 0,
                    "average_cpc": random.randint(5000000, 50000000),  # CPC in micros
                    "cost_per_conversion": round((cost_micros / 1000000) / conversions, 2) if conversions > 0 else 0,
                    "value_per_conversion": round(conversion_value / conversions, 2) if conversions > 0 else 0,
                    "campaign_status": random.choice(["ENABLED", "PAUSED"]),
                    "campaign_type": random.choice(["SEARCH", "DISPLAY", "SHOPPING", "VIDEO"]),
                    "bidding_strategy": random.choice(["TARGET_CPA", "TARGET_ROAS", "MAXIMIZE_CONVERSIONS"]),
                    "platform": "google"
                }
                campaigns.append(campaign)
        
        await bigquery_client.insert_data("google_campaigns", campaigns)
        
        return {
            "message": "Google Ads demo data generated successfully",
            "data": {
                "campaigns": len(campaigns)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate Google demo data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-shiprocket")
async def generate_shiprocket_demo_data(request: DemoDataRequest = DemoDataRequest()):
    """Generate dummy Shiprocket data"""
    try:
        bigquery_client = BigQueryClient()
        
        # Generate dummy shipments
        shipments = []
        courier_names = ["BlueDart", "DTDC", "Delhivery", "Ecom Express", "FedEx"]
        cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Pune", "Hyderabad"]
        
        for i in range(5000):  # 5000 shipments
            pickup_date = datetime.utcnow() - timedelta(days=random.randint(0, 90))
            delivered_date = pickup_date + timedelta(days=random.randint(1, 7)) if random.choice([True, False]) else None
            
            shipment = {
                "shipment_id": f"shipment_{i+1}",
                "order_id": f"order_{random.randint(1, 1000)}",
                "awb": f"AWB{random.randint(100000000, 999999999)}",
                "courier_name": random.choice(courier_names),
                "status": random.choice(["DELIVERED", "IN_TRANSIT", "PICKED_UP", "RETURNED"]),
                "pickup_date": pickup_date.date().strftime("%Y-%m-%d"),
                "delivered_date": delivered_date.date().strftime("%Y-%m-%d") if delivered_date else None,
                "expected_delivery_date": (pickup_date + timedelta(days=random.randint(2, 5))).date().strftime("%Y-%m-%d"),
                "shipping_charges": round(random.uniform(30.0, 200.0), 2),
                "cod_charges": round(random.uniform(0.0, 50.0), 2),
                "weight": round(random.uniform(0.1, 5.0), 2),
                "length": round(random.uniform(10.0, 50.0), 1),
                "breadth": round(random.uniform(10.0, 30.0), 1),
                "height": round(random.uniform(5.0, 20.0), 1),
                "pickup_address": json.dumps({
                    "city": random.choice(cities),
                    "state": "Maharashtra",
                    "pincode": f"{random.randint(400000, 499999)}"
                }),
                "delivery_address": json.dumps({
                    "city": random.choice(cities),
                    "state": random.choice(["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi"]),
                    "pincode": f"{random.randint(100000, 999999)}"
                }),
                "tracking_data": json.dumps({
                    "current_status": random.choice(["Out for delivery", "In transit", "Delivered"]),
                    "last_update": pickup_date.isoformat()
                }),
                "platform": "shiprocket"
            }
            shipments.append(shipment)
        
        await bigquery_client.insert_data("shiprocket_shipments", shipments)
        
        return {
            "message": "Shiprocket demo data generated successfully",
            "data": {
                "shipments": len(shipments)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate Shiprocket demo data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-all")
async def generate_all_demo_data(request: DemoDataRequest = DemoDataRequest()):
    """Generate all demo data"""
    try:
        # Generate data for all platforms
        shopify_result = await generate_shopify_demo_data(request)
        facebook_result = await generate_facebook_demo_data(request)
        google_result = await generate_google_demo_data(request)
        shiprocket_result = await generate_shiprocket_demo_data(request)
        
        return {
            "message": "All demo data generated successfully",
            "data": {
                "shopify": shopify_result["data"],
                "facebook": facebook_result["data"],
                "google": google_result["data"],
                "shiprocket": shiprocket_result["data"]
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to generate all demo data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analytics")
async def get_demo_analytics(request: Dict[str, Any]):
    """Get demo analytics data for dashboard"""
    try:
        platforms = request.get("platforms", ["all"])
        time_range = request.get("timeRange", "30d")
        
        # Generate realistic demo analytics
        demo_analytics = {
            "summary": {
                "totalRevenue": 2847650.75,
                "totalOrders": 8945,
                "totalCustomers": 3421,
                "avgOrderValue": 318.45,
                "grossProfit": 1423825.38,
                "netProfit": 854295.23,
                "grossMargin": 50.02,
                "netMargin": 30.01,
                "roas": 4.25,
                "cac": 125.50,
                "ltv": 1250.75
            },
            "timeSeriesData": [
                {
                    "date": "2024-01-01",
                    "totalRevenue": 95000.50,
                    "orders": 298,
                    "customers": 156,
                    "adSpend": 22500.25,
                    "conversions": 89,
                    "newCustomers": 45
                },
                {
                    "date": "2024-01-02", 
                    "totalRevenue": 87500.75,
                    "orders": 275,
                    "customers": 142,
                    "adSpend": 20750.50,
                    "conversions": 82,
                    "newCustomers": 38
                },
                # Add more time series data...
            ],
            "platformBreakdown": {
                "shopify": {
                    "revenue": 2847650.75,
                    "orders": 8945,
                    "customers": 3421,
                    "conversionRate": 3.45
                },
                "facebook": {
                    "spend": 425000.50,
                    "impressions": 12500000,
                    "clicks": 125000,
                    "conversions": 4250,
                    "ctr": 1.0,
                    "cpc": 3.40,
                    "roas": 6.70
                },
                "google": {
                    "spend": 385000.25,
                    "impressions": 8750000,
                    "clicks": 87500,
                    "conversions": 3500,
                    "ctr": 1.0,
                    "cpc": 4.40,
                    "roas": 7.40
                },
                "shiprocket": {
                    "shipments": 8945,
                    "delivered": 8234,
                    "avgDeliveryTime": 3.2,
                    "shippingCost": 178900.50,
                    "deliveryRate": 92.05
                }
            },
            "d2cMetrics": {
                "revenueMetrics": {
                    "totalRevenue": 2847650.75,
                    "avgOrderValue": 318.45,
                    "revenuePerChannel": {
                        "organic": 1138706.30,
                        "paid": 1423825.38,
                        "social": 285119.07
                    },
                    "gmv": 2847650.75,
                    "subscriptionRevenue": 142382.54,
                    "refundAmount": 56953.02
                },
                "costMetrics": {
                    "cogs": 1423825.38,
                    "opex": 284765.08,
                    "adSpend": 810000.75,
                    "marketplaceFees": 85429.52,
                    "shippingCosts": 178900.50,
                    "paymentGatewayFees": 42714.76,
                    "returnProcessingCosts": 28476.51,
                    "overheadCosts": 142382.54
                },
                "profitMetrics": {
                    "grossProfit": 1423825.38,
                    "netProfit": 854295.23,
                    "grossMargin": 50.02,
                    "netMargin": 30.01,
                    "ebit": 996677.77,
                    "operatingProfit": 854295.23
                },
                "customerMetrics": {
                    "cac": 125.50,
                    "clv": 1250.75,
                    "repeatPurchaseRate": 35.5,
                    "churnRate": 8.2,
                    "newCustomerCount": 1368,
                    "returningCustomerCount": 2053,
                    "retentionRate": 91.8,
                    "nps": 72,
                    "satisfactionScore": 4.3
                },
                "inventoryMetrics": {
                    "inventoryTurnover": 8.5,
                    "stockoutRate": 2.1,
                    "daysToSellInventory": 43,
                    "inventoryValue": 1423825.38,
                    "overstockRate": 5.2,
                    "stockAccuracy": 97.8
                },
                "websiteMetrics": {
                    "sessions": 425000,
                    "bounceRate": 45.2,
                    "avgSessionDuration": 185,
                    "pageViews": 1275000,
                    "uniqueVisitors": 325000,
                    "exitRate": 38.5,
                    "pagesPerSession": 3.0,
                    "ttfb": 1.2,
                    "cartAbandonmentRate": 68.5
                }
            },
            "adMetrics": {
                "performanceMetrics": {
                    "impressions": 21250000,
                    "clicks": 212500,
                    "clickThroughRate": 1.0,
                    "costPerClick": 3.81,
                    "conversions": 7750,
                    "conversionRate": 3.65,
                    "costPerConversion": 104.52,
                    "returnOnAdSpend": 6.98,
                    "advertisingCostOfSales": 14.32,
                    "costPerMille": 38.12,
                    "costPerAction": 104.52
                },
                "engagementMetrics": {
                    "likes": 85000,
                    "shares": 12750,
                    "comments": 8500,
                    "videoViews": 1275000,
                    "videoCompletionRate": 65.5,
                    "engagementRate": 4.8
                },
                "campaignMetrics": {
                    "adReach": 8500000,
                    "frequency": 2.5,
                    "qualityScore": 8.2,
                    "adPosition": 1.8,
                    "clickToOpenRate": 12.5
                }
            },
            "deliveryMetrics": {
                "shippingMetrics": {
                    "avgDeliveryTime": 3.2,
                    "shippingCostPerOrder": 20.0,
                    "onTimeDeliveryRate": 92.05,
                    "lateDeliveryRate": 7.95,
                    "failedDeliveryAttempts": 178,
                    "returnRate": 4.2,
                    "returnProcessingTime": 2.5,
                    "pickupSuccessRate": 98.5
                },
                "costMetrics": {
                    "totalShippingCost": 178900.50,
                    "fuelSurcharge": 8945.03,
                    "handlingFees": 4472.51,
                    "insuranceCosts": 2236.26
                },
                "performanceMetrics": {
                    "deliveryDistance": 450.5,
                    "packageVolume": 8945,
                    "courierEfficiency": 94.2,
                    "customerComplaintRate": 1.8
                }
            }
        }
        
        return demo_analytics
        
    except Exception as e:
        logger.error(f"Failed to get demo analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))