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
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class MetricData(BaseModel):
    date: datetime
    value: float
    platform: str

class DashboardMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    avg_order_value: float
    conversion_rate: float
    roas: float
    acos: float

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

class PlatformMetrics(BaseModel):
    platform: str
    revenue: float
    orders: int
    roas: float
    spend: float

class Integration(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    platform: str
    credentials: Dict[str, Any]
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_sync: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class IntegrationCreate(BaseModel):
    platform: str
    credentials: Dict[str, Any]

class IntegrationResponse(BaseModel):
    id: str
    platform: str
    is_active: bool
    created_at: datetime
    last_sync: Optional[datetime] = None
