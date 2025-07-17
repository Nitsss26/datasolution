from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum

class TimeRange(str, Enum):
    LAST_7_DAYS = "7d"
    LAST_15_DAYS = "15d"
    LAST_30_DAYS = "30d"
    LAST_90_DAYS = "90d"

class Platform(str, Enum):
    SHOPIFY = "shopify"
    FACEBOOK_ADS = "facebook_ads"
    GOOGLE_ADS = "google_ads"
    SHIPROCKET = "shiprocket"
    AMAZON = "amazon"
    FLIPKART = "flipkart"

class MetricType(str, Enum):
    REVENUE = "revenue"
    ORDERS = "orders"
    AOV = "aov"
    ROAS = "roas"
    ACOS = "acos"
    CAC = "cac"
    SESSIONS = "sessions"
    CONVERSION_RATE = "conversion_rate"

class AnalyticsRequest(BaseModel):
    platforms: List[Platform]
    time_range: TimeRange
    metrics: List[MetricType]

class MetricData(BaseModel):
    metric: MetricType
    value: float
    change_percentage: Optional[float] = None
    platform: Optional[Platform] = None

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

class DashboardData(BaseModel):
    metrics: List[MetricData]
    charts: Dict[str, ChartData]
    last_updated: datetime = datetime.utcnow()

class IntegrationConfig(BaseModel):
    platform: Platform
    api_key: str
    additional_config: Optional[Dict[str, Any]] = {}
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
