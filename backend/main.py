from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import routers
from routers import auth, dashboard, integrations, analytics
from database import init_db
from utils.auth import verify_token

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    await init_db()
    yield

app = FastAPI(
    title="D2C Analytics API",
    description="All-in-One D2C Data Solution",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)])
app.include_router(integrations.router, prefix="/api/integrations", tags=["Integrations"], dependencies=[Depends(get_current_user)])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"], dependencies=[Depends(get_current_user)])

@app.get("/")
async def root():
    return {"message": "D2C Analytics API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
