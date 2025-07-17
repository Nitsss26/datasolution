from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from models.user import UserCreate, UserLogin, User
from utils.auth import verify_password, get_password_hash, create_access_token
from database import get_database
from datetime import datetime, timedelta
import re

router = APIRouter()
security = HTTPBearer()

@router.post("/register")
async def register(user: UserCreate):
    db = await get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password strength
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user
    user_data = {
        "email": user.email,
        "password": hashed_password,
        "company_name": user.company_name,
        "full_name": user.full_name,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = await db.users.insert_one(user_data)
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(result.inserted_id),
            "email": user.email,
            "company_name": user.company_name,
            "full_name": user.full_name
        }
    }

@router.post("/login")
async def login(user: UserLogin):
    db = await get_database()
    
    # Find user
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(db_user["_id"]),
            "email": db_user["email"],
            "company_name": db_user["company_name"],
            "full_name": db_user["full_name"]
        }
    }
