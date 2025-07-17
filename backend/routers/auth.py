from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserCreate, UserLogin, User, UserInDB, Token
from utils.auth import get_password_hash, verify_password, create_access_token, verify_token
from database import get_database
from datetime import timedelta
import pymongo

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    db = get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict.pop("password")
    user_dict["hashed_password"] = hashed_password
    
    result = await db.users.insert_one(user_dict)
    
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    db = get_database()
    
    # Find user
    user = await db.users.find_one({"email": user_credentials.email})
    if not user or not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=dict)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    db = get_database()
    
    # Verify token
    token_data = await verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    user = await db.users.find_one({"email": token_data["email"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "company_name": user.get("company_name"),
        "is_active": user.get("is_active", True)
    }
