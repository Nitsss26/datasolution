from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from models.user import UserCreate, UserLogin, User, UserInDB, Token
from utils.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_collection

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    users_collection = await get_collection("users")
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    del user_dict["password"]
    user_dict["hashed_password"] = hashed_password
    
    result = await users_collection.insert_one(user_dict)
    
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    users_collection = await get_collection("users")
    
    # Find user
    user = await users_collection.find_one({"email": user_credentials.email})
    if not user or not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def get_current_user(email: str = Depends(verify_token)):
    users_collection = await get_collection("users")
    
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(
        id=str(user["_id"]),
        email=user["email"],
        full_name=user["full_name"],
        company_name=user.get("company_name"),
        is_active=user["is_active"],
        created_at=user["created_at"],
        updated_at=user["updated_at"]
    )
