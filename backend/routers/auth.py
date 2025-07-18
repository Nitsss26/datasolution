from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import bcrypt
from datetime import datetime
import secrets
from database import get_database

router = APIRouter()

# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    company_name: Optional[str] = None
    created_at: datetime
    is_active: bool = True

@router.post("/register")
async def register_user(user_data: UserRegister):
    """Register a new user"""
    try:
        db = await get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), salt)
        
        # Create user document
        user_doc = {
            "email": user_data.email,
            "password": hashed_password.decode('utf-8'),
            "full_name": user_data.full_name,
            "company_name": user_data.company_name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True,
            "api_key": secrets.token_urlsafe(32)
        }
        
        # Insert user
        result = await db.users.insert_one(user_doc)
        
        # Return success response
        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id),
            "email": user_data.email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login")
async def login_user(user_data: UserLogin):
    """Login user"""
    try:
        db = await get_database()
        
        # Find user
        user = await db.users.find_one({"email": user_data.email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Check password
        if not bcrypt.checkpw(user_data.password.encode('utf-8'), user["password"].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(status_code=401, detail="Account is disabled")
        
        # Update last login
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Return success response
        return {
            "message": "Login successful",
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "full_name": user["full_name"],
                "company_name": user.get("company_name"),
                "api_key": user["api_key"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/profile")
async def get_user_profile():
    """Get user profile (placeholder - needs authentication middleware)"""
    return {"message": "Profile endpoint - authentication needed"}

@router.post("/logout")
async def logout_user():
    """Logout user"""
    return {"message": "Logout successful"}