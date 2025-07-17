from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    company_name: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    company_name: str
    full_name: str
    created_at: datetime
    is_active: bool = True
    
    class Config:
        json_encoders = {
            ObjectId: str
        }

class UserIntegration(BaseModel):
    user_id: str
    platform: str  # shopify, facebook_ads, google_ads, shiprocket
    credentials: dict
    is_active: bool = True
    created_at: datetime
    last_sync: Optional[datetime] = None
