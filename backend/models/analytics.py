from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PlatformType(str, Enum):
    SHOPIFY = "shopify"
    FACEBOOK_ADS = "facebook_ads"
    GOOGLE_ADS = "google_ads"
    SHIPROCKET = "shiprocket"

class TimeRange(str, Enum):
    DAYS_7 = "7d"
    DAYS_15 = "15d"
    DAYS_30 = "30d"
    DAYS_90 = "90d"

class AnalyticsData(BaseModel):
    user_id: str
    platform: PlatformType
    date: datetime
    metrics: Dict[str, Any]
    raw_data: Optional[Dict[str, Any]] = None

class DashboardMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    avg_order_value: float
    total_ad_spend: float
    roas: float
    conversion_rate: float
    total_sessions: int
    bounce_rate: float
    
class PlatformMetrics(BaseModel):
    platform: str
    revenue: float
    orders: int
    sessions: int
    conversion_rate: float
