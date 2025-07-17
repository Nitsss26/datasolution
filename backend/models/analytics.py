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
