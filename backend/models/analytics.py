from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class MetricData(BaseModel):
    value: float
    change: float
    trend: str  # "up", "down", "stable"

class ChartDataPoint(BaseModel):
    date: str
    value: float
    label: Optional[str] = None

class PlatformMetric(BaseModel):
    platform: str
    revenue: float
    orders: int
    aov: float
    roas: Optional[float] = None

class Integration(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    platform: str
    platform_name: str
    status: str  # "connected", "disconnected", "error"
    credentials: Dict[str, Any]
    last_sync: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CustomerSegment(BaseModel):
    segment: str
    count: int
    revenue: float
    percentage: float

class ProductPerformance(BaseModel):
    product_name: str
    revenue: float
    units_sold: int
    profit_margin: float

class AnalyticsData(BaseModel):
    """Main analytics data structure"""
    platforms: List[str]
    time_range: str
    total_revenue: float
    total_orders: int
    total_customers: int
    avg_order_value: float
    customer_acquisition_cost: float
    return_on_ad_spend: float
    conversion_rate: float
    platform_breakdown: List[PlatformMetric]
    time_series_data: List[ChartDataPoint]
    customer_segments: List[CustomerSegment]
    product_performance: List[ProductPerformance]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class PlatformData(BaseModel):
    """Platform-specific data structure"""
    platform: str
    platform_name: str
    connected: bool
    last_sync: Optional[datetime] = None
    data_points: int = 0
    metrics: Dict[str, Any] = {}
    status: str = "disconnected"  # "connected", "disconnected", "error"

class UserPreferences(BaseModel):
    """User preferences data structure"""
    user_id: str = "default"
    selected_platforms: List[str] = ["all"]
    default_time_range: str = "30d"
    favorite_charts: List[str] = []
    theme: str = "system"  # "light", "dark", "system"
    ai_enabled: bool = True
    dashboard_layout: List[Dict[str, Any]] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)
