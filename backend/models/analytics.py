from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
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
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class MetricData(BaseModel):
    date: datetime
    value: float
    platform: str
    metric_type: str

class DashboardMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    average_order_value: float
    conversion_rate: float
    return_on_ad_spend: float
    customer_acquisition_cost: float

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

class PlatformMetrics(BaseModel):
    platform: str
    revenue: float
    orders: int
    aov: float
    roas: float
    spend: float

class Integration(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    platform: str
    platform_name: str
    is_connected: bool = False
    credentials: Dict[str, Any] = {}
    last_sync: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class IntegrationCreate(BaseModel):
    platform: str
    credentials: Dict[str, Any]

class IntegrationUpdate(BaseModel):
    credentials: Optional[Dict[str, Any]] = None
    is_connected: Optional[bool] = None
